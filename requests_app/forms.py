from django import forms
from .models import Request

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['request_type', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'request_type': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'request_type': 'Тип обращения',
            'description': 'Подробное описание',
        }