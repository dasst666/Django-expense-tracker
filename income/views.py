from django.shortcuts import render
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, TemplateView
from .models import Income, IncomeCategory
from django.db.models import Sum
from django.urls import reverse_lazy
from .forms import IncomeForm, IncomeCategoryForm
from datetime import date
from django.db.models.functions import TruncMonth
import calendar


class IncomeListView(ListView):
    model = Income
    template_name = "income_list.html"
    context_object_name = 'incomes'
    paginate_by = 5

    def get_queryset(self):
        return Income.objects.all()
    
    def get_total_income(self):
        return self.get_queryset().aggregate(total=Sum('amount'))['total'] or 0
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_income'] = self.get_total_income()
        return context

class IncomeCreateView(CreateView):
    model = Income
    form_class = IncomeForm
    template_name = "main/create_form.html"
    success_url = reverse_lazy('income:income_add')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Income'
        context['category_url'] = 'income:income_category_add'
        return context
    
    def form_valid(self, form):
        return super().form_valid(form)

class IncomeCategoryCreateView(CreateView):
    model = IncomeCategory
    form_class = IncomeCategoryForm
    template_name = "main/create_category_form.html"
    sucess_url = reverse_lazy('income:income_category_add')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'income' 
        context["back_url"] = 'income:income_add'
        context["title"] = 'Add Income Category'
        return context
    
    def form_valid(self, form):
        return super().form_valid(form)

class IncomeDeleteView(DeleteView):
    model = Income
    template_name = "main/confirm_delete.html"
    success_url = reverse_lazy('income:income_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["item_type"] = "доход"
        context["cancel_url"] = "income:income_list"
        return context
    

class IncomeUpdateView(UpdateView):
    model = Income
    form_class = IncomeForm
    template_name = "income/income_form.html"
    success_url = reverse_lazy('income:income_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Изменить? {self.object.category} {self.object.amount}'
        return context

class IncomeMonthlyView(TemplateView):
    model = Income
    template_name = "income/income_monthly.html"
    success_url = reverse_lazy('income:income_monthly')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_year = date.today().year
        income = Income.objects.filter(date__year=current_year)
        monthly_incomes = (
            income
            .annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(total=Sum('amount'))
        )
        total_year_incomes = sum(item['total'] for item in monthly_incomes)
        month_count = len(monthly_incomes)
        avg_year_incomes = round(total_year_incomes/month_count, 2) if month_count > 0 else 0

        monthly_incomes_for_plot = (
            monthly_incomes
            .order_by('month')
        )
        labels = []
        data = []
        for entry in monthly_incomes_for_plot:
            month_date = entry['month']
            month_name = calendar.month_name[month_date.month]
            labels.append(month_name)
            data.append(float(entry['total']))

        context['avg_year_incomes'] = avg_year_incomes
        context['monthly_incomes_for_plot'] = monthly_incomes_for_plot
        context['labels'] = labels
        context['data'] = data
        return context
    


    
    


    

