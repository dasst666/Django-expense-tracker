from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from django.views.generic import TemplateView, ListView, CreateView
from django.utils import timezone
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib import messages
from django.db.models.functions import TruncMonth
from django.db import IntegrityError, transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Category, Transaction
from income.models import Income
from expense.models import Expense
from datetime import timedelta, datetime, date
import calendar


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "main/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # expenses for last 7 days (last week)
        last_7_days = timezone.now() - timedelta(days=7)
        last_7_days_expenses = Expense.objects.filter(date__gte=last_7_days)

        total_last_7_days_expenses = last_7_days_expenses.aggregate(total=Sum('amount'))['total'] or 0
        total_income = Income.objects.aggregate(total=Sum('amount'))['total'] or 0
        total_expense = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0
        balance = total_income - total_expense

        context.update({
            'total_last_7_days_expenses': round(total_last_7_days_expenses, 2),
            'total_income': round(total_income, 2),
            'total_expense': round(total_expense, 2),
            'balance': round(balance, 2),
        })
        return context

class BaseListView(ListView):
    model = None
    category_model = None
    type_label = ''
    urls_namespace = ''

    template_name = "main/list.html"
    context_object_name = 'transactions'
    paginate_by = 5

    def get_queryset(self):
        category_id = self.request.GET.get('category')
        queryset = self.model.objects.all().order_by('-date')

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset
    
    def get_total_income(self):
        return self.get_queryset().aggregate(total=Sum('amount'))['total'] or 0
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'total_income': self.get_total_income(),
            'categories': self.category_model.objects.all(),
            'monthly_url': f'{self.urls_namespace}:{self.urls_namespace}_monthly',
            'type': self.type_label,
            'delete_url': f'{self.urls_namespace}:{self.urls_namespace}_delete',
            'cancel_url': f'{self.urls_namespace}:{self.urls_namespace}_update',
        })
        return context

class BaseMonthlyView(TemplateView):
    template_name = "main/monthly_barplot.html"

    model = None
    type_label = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Monthly total expenses like month: January, total: 200000
        current_year = date.today().year
        queryset = self.model.objects.filter(date__year=current_year)
        monthly_data = (
            queryset
            .annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(total=Sum('amount'))
        )
        # Calculating avg monthly expenses for this year
        total_year_transactions = sum(item['total'] for item in monthly_data)
        month_count = len(monthly_data)
        avg_year_transactions = round(total_year_transactions/month_count, 2) if month_count > 0 else 0
        # Monthly total expenses sorted for plot
        monthly_data_for_plot = (
            monthly_data
            .order_by('month')
        )
        labels = []
        data = []
        for entry in monthly_data_for_plot:
            month_date = entry['month']
            month_name = calendar.month_name[month_date.month]
            labels.append(month_name)
            data.append(float(entry['total']))

        context['avg_year'] = avg_year_transactions
        context['monthly_data_for_plot'] = monthly_data_for_plot
        context['labels'] = labels 
        context['data'] = data
        context['type'] = self.type_label
        return context
    
class BaseTransactionCreateView(CreateView):
    model = None
    form_class = None
    urls_namespace = ''
    template_name = "main/create_form.html"
    def get_success_url(self):
        return reverse(f'{self.urls_namespace}:{self.urls_namespace}_add')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = f'Add {self.urls_namespace.title()}'
        context['category_url'] = f'{self.urls_namespace}:{self.urls_namespace}_category_add'
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class BaseCategoryCreateView(CreateView):
    model = None
    form_class = None
    urls_namespace = ''
    template_name = "main/create_category_form.html"

    def get_success_url(self):
        return reverse(f'{self.urls_namespace}:{self.urls_namespace}_category_add')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            "title": f'Add {self.urls_namespace.title()} Category',
            'type': self.urls_namespace,
            'back_url': f'{self.urls_namespace}:{self.urls_namespace}_add',
        })
        return context
    
    def form_invalid(self, form):
        name_errors = form.errors.get('name')
        if name_errors:
            for error in name_errors:
                messages.warning(self.request, f"Ошибка: категория с таким именем уже существует.")
        return super().form_invalid(form)
