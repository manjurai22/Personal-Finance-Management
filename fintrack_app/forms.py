from django import forms
from .models import Budget, Debt, UserProfile

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

class DebtForm(forms.ModelForm):
    class Meta:
        model = Debt
        fields = [
            'title',
            'debt_type',
            'total_amount',
            'remaining_amount',
            'start_date',
            'due_date'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'debt_type': forms.Select(attrs={'class': 'form-select'}),
            'total_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'remaining_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
