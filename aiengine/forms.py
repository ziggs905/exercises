from django import forms


class GenerateRecipeForm(forms.Form):
    preferences = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
        label='Preferences (optional)',
    )
