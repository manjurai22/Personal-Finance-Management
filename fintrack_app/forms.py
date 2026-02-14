from django import forms
from .models import Budget

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['monthly_limit', 'month']
        widgets = {
            'month': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'monthly_limit': forms.NumberInput(attrs={'class': 'form-control'}),
        }
