from django.shortcuts import render, get_object_or_404
from .models import Category, Transaction
from django.core.paginator import Paginator

from income.models import Income
from expense.models import Expense
from django.db.models import Sum
from django.views.generic import TemplateView
from django.utils import timezone
from datetime import timedelta, datetime
from django.db.models.functions import TruncMonth
import calendar

def transaction_list(request, category_slug=None):
    page = request.GET.get('page', 1)
    category = None
    categories = Category.objects.all()
    transactions = Transaction.objects.filter()
    paginator = Paginator(transactions, 5)
    current_page = paginator.page(int(page))
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        paginator = Paginator(transactions.filter(category=category), 5)
        current_page = paginator.page(int(page))
    return render(request,
                    'main/transaction/list.html',
                    {'category': category,
                    'categories': categories,
                    'transactions': current_page,
                    'slug_url': category_slug})

class DashboardView(TemplateView):
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

        context['total_last_7_days_expenses'] = total_last_7_days_expenses
        context["total_income"] = total_income
        context["total_expense"] = total_expense
        context["balance"] = balance

        return context
    


