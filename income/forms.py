from django import forms
from .models import Income, IncomeCategory
from main.forms import BaseTransactionForm, BaseTransactionCategoryForm

class IncomeForm(BaseTransactionForm):
    class Meta(BaseTransactionForm.Meta):
        model = Income
        

class IncomeCategoryForm(BaseTransactionCategoryForm):
    class Meta(BaseTransactionCategoryForm.Meta):
        model = IncomeCategory