from django import forms

from recipes.models import Recipe


class GenerateRecipeForm(forms.Form):
    meal_type = forms.ChoiceField(choices=Recipe.MealType.choices, label='Meal type')
    preferences = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
        label='Preferences (optional)',
    )
