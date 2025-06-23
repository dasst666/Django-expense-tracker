from django import forms
from .models import Expense, ExpenseCategory, ExpenseCategoryLimit
from main.forms import BaseTransactionForm, BaseTransactionCategoryForm

class ExpenseForm(BaseTransactionForm):
    class Meta(BaseTransactionForm.Meta):
        model = Expense

class ExpenseCategoryForm(BaseTransactionCategoryForm):
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