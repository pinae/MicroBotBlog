from django import forms
from .models import BlogImage


class ImageForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = BlogImage
        fields = ('image',)
