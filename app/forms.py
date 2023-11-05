from django import forms
from django.forms import ModelForm
from .models import ImageModel


class ImageForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = ('name', 'description', 'image')
