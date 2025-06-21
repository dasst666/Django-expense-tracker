from django import forms
from .models import Income, IncomeCategory
from main.forms import BaseTransactionForm, BaseTransactionCategoryForm

class IncomeForm(forms.ModelForm):
    class Meta(BaseTransactionForm.Meta):
        model = Income
        

class IncomeCategoryForm(forms.ModelForm):
    class Meta(BaseTransactionCategoryForm.Meta):
        model = IncomeCategory