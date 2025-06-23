from django.shortcuts import render
from django.db.models.functions import TruncMonth
from django.utils.timezone import now
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Expense, ExpenseCategory, ExpenseCategoryLimit
from .forms import ExpenseForm, ExpenseCategoryForm, ExpenseCategoryLimitForm
from datetime import datetime
from main.views import BaseMonthlyView, BaseListView, BaseTransactionCreateView, BaseCategoryCreateView
import calendar
import logging

logger = logging.getLogger(__name__)

class ExpenseNamespaceMixin:
    urls_namespace = 'expense'

class ExpenseListView(ExpenseNamespaceMixin, BaseListView):
    model = Expense
    category_model = ExpenseCategory
    type_label = 'расход'

class ExpenseCreateView(ExpenseNamespaceMixin, BaseTransactionCreateView):
    model = Expense
    form_class = ExpenseForm

class ExpenseCategoryCreateView(ExpenseNamespaceMixin, BaseCategoryCreateView):
    model = ExpenseCategory
    form_class = ExpenseCategoryForm
    
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

        try:
            limits = ExpenseCategoryLimit.objects.filter(month__year=year, month__month=month)
            if not limits.exists():
                messages.warning(self.request, "На этот месяц нет установленных лимитов по категориям.")
                context['category_statuses'] = []
                return context

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
                try:
                    percent = round((spent / limit.limit) * 100)
                except ZeroDivisionError:
                    percent = 0
                    logger.warning(f"Деление на ноль в лимите категории: {limit.category}")
                    messages.warning(self.request, f"Лимит категории '{limit.category}' равен 0 — деление на ноль.")

                category_statuses.append({
                    'category': limit.category.name,
                    'limit': limit.limit,
                    'spent': spent,
                    'percent': percent,
                    'limit_obj': limit 
                })

            context['category_statuses'] = category_statuses
        except Exception as e:
            logger.exception("Ошибка при загрузке лимитов расходов:")
            context['error'] = "Произошла ошибка при загрузке данных. Пожалуйста, попробуйте позже."
            context['category_statuses'] = []

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


    

    




     
    



    
    
