from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Expense, ExpenseCategory, ExpenseCategoryLimit
from django.db.models import Sum
from .forms import ExpenseForm, ExpenseCategoryForm, ExpenseCategoryLimitForm, ExpenseCategoryFilterForm
from django.urls import reverse_lazy
from datetime import timedelta, datetime, date
from django.db.models.functions import TruncMonth
import calendar
from django.utils.timezone import now
from django.contrib import messages
from django.shortcuts import redirect
from main.views import BaseMonthlyView, BaseListView, BaseTransactionCreateView

class ExpenseListView(BaseListView):
    model = Expense
    category_model = ExpenseCategory
    type_label = 'расход'
    urls_namespace = 'expense'

class ExpenseCreateView(BaseTransactionCreateView):
    model = Expense
    form_class = ExpenseForm
    urls_namespace = 'expense'

class ExpenseCategoryCreateView(CreateView):
    model = ExpenseCategory
    form_class = ExpenseCategoryForm
    template_name = "main/create_category_form.html"
    success_url = reverse_lazy('expense:expense_category_add')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Add Expense Category'
        context['type'] = 'expense'
        context['back_url'] = 'expense:expense_add'
        return context
    
    def form_valid(self, form):
        return super().form_valid(form)
    
class ExpenseDeleteView(DeleteView):
    model = Expense
    template_name = "main/confirm_delete.html"
    success_url = reverse_lazy('expense:expense_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["item_type"] = "расход"
        context["cancel_url"] = "expense:expense_list"
        return context
    

class ExpenseUpdateView(UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = "expense/expense_form.html"
    success_url = reverse_lazy('expense:expense_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Edit Expense: {self.object.category} {self.object.amount}'
        return context

class ExpenseCategoryPieView(TemplateView):
    template_name = "expense/expense_category_pie.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем выбранный месяц из GET-параметра
        selected_month = self.request.GET.get('month')
        if selected_month:
            try:
                year, month = map(int, selected_month.split('-'))
            except ValueError:
                year, month = datetime.today().year, datetime.today().month
        else:
            year, month = datetime.today().year, datetime.today().month

        # Все доступные месяцы с расходами (например: ['2024-04', '2024-03'])
        months_with_data = (
            Expense.objects
            .annotate(month=TruncMonth('date'))
            .values_list('month', flat=True)
            .distinct()
            .order_by('-month')
        )
        month_options = [
            (m.strftime('%Y-%m'), m.strftime('%B %Y'))
            for m in months_with_data
        ]

        # Отфильтрованные расходы по выбранному месяцу
        expenses = Expense.objects.filter(date__year=year, date__month=month)

        category_data = (
            expenses
            .values('category__name')
            .annotate(total=Sum('amount'))
            .order_by('-total')
        )
        pie_labels = [item['category__name'] for item in category_data]
        pie_data = [float(item['total']) for item in category_data]

        total_monthly_expense = expenses.aggregate(total=Sum('amount'))['total'] or 0 
        day_in_month = calendar.monthrange(year, month)[1]
        avg_daily_expenses = round(total_monthly_expense / day_in_month, 2)

        context['total_monthly_expense'] = total_monthly_expense
        context['avg_daily_expenses'] = avg_daily_expenses
        context['selected_month'] = f"{year:04d}-{month:02d}"
        context['month_options'] = month_options
        context['pie_labels'] = pie_labels
        context['pie_data'] = pie_data
        return context
    
class ExpenseMonthlyView(BaseMonthlyView):
    model = Expense
    type_label = 'расход'

class ExpenseCategoryLimitCreateView(CreateView):
    model = ExpenseCategoryLimit
    template_name = "expense/expense_category_limit_form.html"
    form_class = ExpenseCategoryLimitForm
    success_url = reverse_lazy('expense:expense_limit_add')

    def form_valid(self, form):
        instance = form.save(commit=False)
        today = now().date()
        instance.month = today.replace(day=1)

        # If category limit exist
        exists = ExpenseCategoryLimit.objects.filter(
            category=instance.category,
            month=instance.month
        ).exists()
        if exists:
            messages.error(self.request, f"Лимит на категорию {instance.category} за этот месяц уже установлен.")
            return redirect('expense:expense_limit_add') 
        return super().form_valid(form)

class ExpenseCategoryLimitStatusView(TemplateView):
    model = ExpenseCategoryLimit
    template_name = "expense/expense_category_limit_list.html"
    success_url = reverse_lazy('expense:expense_limit')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = now().date()
        year = today.year
        month = today.month

        limits = ExpenseCategoryLimit.objects.filter(month__year=year, month__month=month)

        expenses = (
            Expense.objects
            .filter(date__year=year, date__month=month)
            .values('category')
            .annotate(total_spent=Sum('amount'))
        )
        expense_dict = {item['category']: item['total_spent'] for item in expenses}
        
        category_statuses = []
        for limit in limits:
            spent = expense_dict.get(limit.category.id, 0)
            percent = round((spent/limit.limit) * 100) if limit.limit else 0
            category_statuses.append({
                'category': limit.category.name,
                'limit': limit.limit,
                'spent': spent,
                'percent': percent,
                'limit_obj': limit 
            })

        context['category_statuses'] = category_statuses
        return context
    
class ExpenseCategoryLimitUpdateView(UpdateView):
    model = ExpenseCategoryLimit
    form_class = ExpenseCategoryLimitForm
    template_name = "expense/expense_category_limit_form.html"
    success_url = reverse_lazy('expense:expense_limit')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f'Edit expense category limit {self.object.category} {self.object.limit}'
        return context

class ExpenseCategoryLimitDeleteView(DeleteView):
    model = ExpenseCategoryLimit
    template_name = "expense/expense_category_limit_confirm_delete.html"
    success_url = reverse_lazy('expense:expense_limit')


    

    




     
    



    
    
