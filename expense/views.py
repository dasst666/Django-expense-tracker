from django.shortcuts import render
from django.views.generic import ListView, CreateView
from .models import Expense
from django.db.models import Sum
from .forms import ExpenseForm
from django.urls import reverse_lazy


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
     
    



    
    
