from django import forms
from .models import Income, IncomeCategory
from bootstrap_datepicker_plus.widgets import DatePickerInput

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'date', 'category', 'note']
        widgets = {
            'date': DatePickerInput(
                options={
                    "format": "YYYY-MM-DD",
                }
            ),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class IncomeCategoryForm(forms.ModelForm):
    class Meta:
        model = IncomeCategory
        fields = ['name']