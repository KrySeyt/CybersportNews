from django import forms

from .models import New


class NewForm(forms.ModelForm):
    class Meta:
        model = New
        fields = ['title', 'text', 'image_url', 'category', 'is_published']
        widgets = {
            'text': forms.Textarea()
        }
