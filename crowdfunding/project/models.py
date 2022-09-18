from django.db import models
from categories.models import Category

# Create your models here.
class Project(models.Model):
    project_title = models.CharField(max_length=100, help_text='Project title should not exceed 100 character.')
    project_category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    project_details = models.TextField(null=True)
    # project_images = models.ImageField()
    project_total_target = models.IntegerField(null=True)
    project_start_date = models.DateField(null=True, blank=True)
    project_end_date = models.DateField(null=True, blank=True) 

    def __str__(self):
        return self.project_title