from django import forms
from django.contrib.auth import get_user_model
from .models import UserSettings

User = get_user_model()

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class SettingsForm(forms.ModelForm):
    class Meta:
        model = UserSettings
        fields = ['email_notifications', 'avatar']  # удалили 'color_scheme'
        widgets = {
            'email_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }