from django import forms

from .models import Cookbook


class CookbookForm(forms.ModelForm):
    class Meta:
        model = Cookbook
        fields = ['name']


class AddToCookbookForm(forms.Form):
    cookbook = forms.ModelChoiceField(
        queryset=Cookbook.objects.none(), required=False, label='Add to existing cookbook',
    )
    new_cookbook_name = forms.CharField(required=False, label='Or create a new cookbook')

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['cookbook'].queryset = Cookbook.objects.filter(owner=user)

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('cookbook') and not cleaned_data.get('new_cookbook_name', '').strip():
            raise forms.ValidationError('Choose an existing cookbook or enter a name for a new one.')
        return cleaned_data
