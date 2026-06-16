from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['weight_kg', 'height_cm', 'age', 'sex', 'activity_level', 'goal', 'allergies']
        widgets = {
            'allergies': forms.Textarea(attrs={'rows': 3}),
        }
