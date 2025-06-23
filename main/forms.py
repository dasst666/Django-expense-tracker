from django import forms
from bootstrap_datepicker_plus.widgets import DateTimePickerInput

# Base form for Expense/Income create
class BaseTransactionForm(forms.ModelForm):
    class Meta:
        fields = ['amount', 'date', 'category', 'note']
        widgets = {
            'date': DateTimePickerInput(
                options={
                    "format": "YYYY-MM-DD HH:mm",
                    "useCurrent": True, 
                    "sideBySide": True,
                    "showClose": True,
                    "showClear": True,
                    "showTodayButton": True,
                }
            ),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        print(f"[DEBUG] Валидация amount: {amount}")
        if amount <= 0:
            raise forms.ValidationError("Сумма должна быть больше 0.")
        return amount

class BaseTransactionCategoryForm(forms.ModelForm):
    class Meta:
        fields = ['name']
    
