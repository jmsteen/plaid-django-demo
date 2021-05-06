from django import forms
from .models import Budget, Category, BudgetCategoryAmount

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['date', 'user']
    
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['description', 'user']

class BudgetCategoryAmountForm(forms.ModelForm):
    class Meta:
        model = BudgetCategoryAmount
        fields = ['amount']