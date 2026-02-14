from django import forms
from .models import Budget, Debt

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
        fields = ['title', 'debt_type', 'total_amount', 'remaining_amount', 'start_date', 'due_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == "debt_type":
                field.widget.attrs.update({'class': 'form-select'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
