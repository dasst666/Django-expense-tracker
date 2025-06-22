from django.shortcuts import render
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, TemplateView
from .models import Income, IncomeCategory
from django.db.models import Sum
from django.urls import reverse_lazy
from .forms import IncomeForm, IncomeCategoryForm
from datetime import date
from django.db.models.functions import TruncMonth
import calendar
from main.views import BaseMonthlyView, BaseListView, BaseTransactionCreateView, BaseCategoryCreateView

class IncomeNamespaceMixin:
    urls_namespace = 'income'

class IncomeListView(BaseListView):
    model = Income
    category_model = IncomeCategory
    type_label = 'доход'

class IncomeCreateView(BaseTransactionCreateView):
    model = Income
    form_class = IncomeForm

class IncomeCategoryCreateView(BaseCategoryCreateView):
    model = IncomeCategory
    form_class = IncomeCategoryForm

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

class IncomeMonthlyView(BaseMonthlyView):
    model = Income
    type_label = 'доход'
    

# TODO: надо написать исключение например такая категория уже создана
    

