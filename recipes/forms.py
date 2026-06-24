from django import forms
from django.forms import inlineformset_factory

from .models import Ingredient, Recipe, Tag


class RecipeForm(forms.ModelForm):
    steps_text = forms.CharField(
        label='Steps (one per line)',
        widget=forms.Textarea(attrs={'rows': 6}),
    )

    class Meta:
        model = Recipe
        fields = [
            'title', 'description', 'servings', 'prep_minutes', 'cook_minutes',
            'calories', 'protein_g', 'carbs_g', 'fat_g', 'tags',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'tags': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['steps_text'].initial = '\n'.join(self.instance.steps)

    def save(self, commit=True):
        recipe = super().save(commit=False)
        recipe.steps = [
            line.strip() for line in self.cleaned_data['steps_text'].splitlines() if line.strip()
        ]
        if commit:
            recipe.save()
            self.save_m2m()
        return recipe


IngredientFormSet = inlineformset_factory(
    Recipe, Ingredient,
    fields=['name', 'quantity', 'unit'],
    extra=3, can_delete=True,
)


class NotesForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['notes']
        widgets = {'notes': forms.Textarea(attrs={'rows': 3})}


class RecipeSearchForm(forms.Form):
    SORT_CHOICES = [
        ('-created_at', 'Newest'),
        ('-rating', 'Highest rating'),
        ('calories', 'Calories'),
        ('title', 'Name'),
    ]

    q = forms.CharField(required=False, label='Search title or ingredient')
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.order_by('category', 'name'),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    max_calories = forms.IntegerField(required=False, min_value=0, label='Max calories')
    min_protein = forms.FloatField(required=False, min_value=0, label='Min protein (g)')
    favorites_only = forms.BooleanField(required=False, label='Favorites only')
    sort = forms.ChoiceField(choices=SORT_CHOICES, required=False, initial='-created_at')
