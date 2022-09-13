from django.db import models

# Create your models here.
class Project(models.Model):
    project_title = models.CharField(max_length=50)