from django import forms

from recipes.models import Recipe

from .models import PlanEntry, WeeklyPlan


class WeeklyPlanForm(forms.ModelForm):
    class Meta:
        model = WeeklyPlan
        fields = ['name', 'start_date']
        widgets = {'start_date': forms.DateInput(attrs={'type': 'date'})}


class SwapRecipeForm(forms.ModelForm):
    class Meta:
        model = PlanEntry
        fields = ['recipe']

    def __init__(self, *args, owner=None, **kwargs):
        super().__init__(*args, **kwargs)
        if owner is not None:
            self.fields['recipe'].queryset = Recipe.objects.filter(owner=owner)
