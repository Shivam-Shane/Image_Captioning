from django import forms
from .models import ImageSaver

class ImageUploadFile(forms.ModelForm):
    class Meta:
        model = ImageSaver
        fields = ['image']
