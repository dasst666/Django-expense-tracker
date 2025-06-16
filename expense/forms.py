from django import forms
from .models import Expense, ExpenseCategory
from bootstrap_datepicker_plus.widgets import DatePickerInput

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'date', 'note', 'category']
        widgets = {
            'date': DatePickerInput(
                options={
                    "format": "YYYY-MM-DD",
                }
            ),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }

class ExpenseCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpenseCategory
        fields = ['name']
