from datetime import date
from pyexpat import model
from django.db import models

# Create your models here.
class Project(models.Model):
    project_title = models.CharField(max_length=100, help_text='Project title should not exceed 100 character.')
    # project_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    project_details = models.TextField(null=True)
    # project_images = models.ImageField()
    project_total_target = models.IntegerField(null=True)
    project_start_date = models.DateField(null=True, blank=True, default=date.today())
    project_end_date = models.DateField(null=True, blank=True) 