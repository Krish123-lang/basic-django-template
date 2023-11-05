from django.db import models

# Create your models here.


class ImageModel(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    image = models.ImageField(null=False, blank=False, upload_to = "images/")

    def __str__(self):
        return self.name
