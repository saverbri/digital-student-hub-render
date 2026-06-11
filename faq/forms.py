from django import forms
from .models import FaqArticle

class FaqArticleForm(forms.ModelForm):
    class Meta:
        model = FaqArticle
        fields = ['title', 'content', 'category', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }