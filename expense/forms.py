from django import forms
from .models import Expense, ExpenseCategory, ExpenseCategoryLimit
from main.forms import BaseTransactionForm, BaseTransactionCategoryForm

class ExpenseForm(forms.ModelForm):
    class Meta(BaseTransactionForm.Meta):
        model = Expense

class ExpenseCategoryForm(forms.ModelForm):
    class Meta(BaseTransactionCategoryForm.Meta):
        model = ExpenseCategory

class ExpenseCategoryLimitForm(forms.ModelForm):
    class Meta:
        model = ExpenseCategoryLimit
        fields = ['category', 'limit']

class ExpenseCategoryFilterForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=ExpenseCategory.objects.all(),
        required=False,
        empty_label="Все категории",
        label = ""
    )