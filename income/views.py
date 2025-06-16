from django.shortcuts import render
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from .models import Income
from django.db.models import Sum
from django.urls import reverse_lazy
from .forms import IncomeForm, IncomeCategoryForm

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
    template_name = "income/income_form.html"
    success_url = reverse_lazy('income:income_add')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Income'
        return context
    
    def form_valid(self, form):
        return super().form_valid(form)

class IncomeDeleteView(DeleteView):
    model = Income
    template_name = "income/income_confirm_delete.html"
    success_url = reverse_lazy('income:income_list')

class IncomeUpdateView(UpdateView):
    model = Income
    template_name = "income/income_form.html"
    success_url = reverse_lazy('income:income_update')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Edit Income: {self.object}'
        return context


    
    


    

