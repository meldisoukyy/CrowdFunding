from distutils.command.upload import upload
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='category/imgs', null=True)

    def __str__(self):
        return self.name