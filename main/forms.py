from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput

# Base form for Expense/Income create
class BaseTransactionForm(forms.ModelForm):
    class Meta:
        fields = ['amount', 'date', 'category', 'note']
        widgets = {
            'date': DatePickerInput(
                options={
                    "format": "YYYY-MM-DD",
                }
            ),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }

class BaseTransactionCategoryForm(forms.ModelForm):
    class Meta:
        fields = ['name']