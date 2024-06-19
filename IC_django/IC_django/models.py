
from django.db import models

class ImageSaver(models.Model):
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Image {self.id}'

    class Meta:
        app_label = 'IC_django'
