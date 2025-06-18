from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Expense, ExpenseCategory
from django.db.models import Sum
from .forms import ExpenseForm, ExpenseCategoryForm
from django.urls import reverse_lazy
from datetime import timedelta, datetime, date
from django.db.models.functions import TruncMonth
import calendar


class ExpenseListView(ListView):
    model = Expense
    template_name = "expense_list.html"
    context_object_name = 'expenses'
    paginate_by = 5

    def get_queryset(self):
        return Expense.objects.all()
    
    def get_total_expenses(self):
        return self.get_queryset().aggregate(total=Sum('amount'))['total'] or 0 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_expense"] = self.get_total_expenses()
        return context

class ExpenseCreateView(CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = "expense/expense_form.html"
    success_url = reverse_lazy('expense:expense_add')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Add Expense'
        return context

    def form_valid(self, form):
        return super().form_valid(form)

class ExpenseCategoryCreateView(CreateView):
    model = ExpenseCategory
    form_class = ExpenseCategoryForm
    template_name = "expense/expense_category_form.html"
    success_url = reverse_lazy('expense:expense_category_add')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Add Expense Category'
        return context
    
    def form_valid(self, form):
        return super().form_valid(form)
    
class ExpenseDeleteView(DeleteView):
    model = Expense
    template_name = "expense/expense_confirm_delete.html"
    success_url = reverse_lazy('expense:expense_list')

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

        context['avg_daily_expenses'] = avg_daily_expenses
        context['selected_month'] = f"{year:04d}-{month:02d}"
        context['month_options'] = month_options
        context['pie_labels'] = pie_labels
        context['pie_data'] = pie_data
        return context
    
class ExpenseMonthlyView(TemplateView):
    model = Expense
    template_name = "expense/expense_monthly.html"
    success_url = reverse_lazy('expese:expense_monthly')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Monthly total expenses like month: January, total: 200000
        current_year = date.today().year
        expense = Expense.objects.filter(date__year=current_year)
        monthly_expenses = (
            expense
            .annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(total=Sum('amount'))
        )
        # Calculating avg monthly expenses for this year
        total_year_expenses = sum(item['total'] for item in monthly_expenses)
        month_count = len(monthly_expenses)
        avg_year_expenses = round(total_year_expenses/month_count, 2) if month_count > 0 else 0
        # Monthly total expenses sorted for plot
        monthly_expenses_for_plot = (
            monthly_expenses
            .order_by('month')
        )
        labels = []
        data = []
        for entry in monthly_expenses_for_plot:
            month_date = entry['month']
            month_name = calendar.month_name[month_date.month]
            labels.append(month_name)
            data.append(float(entry['total']))

        context['avg_year_expenses'] = avg_year_expenses
        context['monthly_expenses_for_plot'] = monthly_expenses_for_plot
        context['labels'] = labels
        context['data'] = data
        return context

def avg_year_expenses(requset):
    expenses = Expense.objects.all()

    avg_year_expense = expenses/ month



     
    



    
    
