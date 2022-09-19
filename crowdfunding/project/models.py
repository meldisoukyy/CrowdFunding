from django.db import models
from django.shortcuts import get_list_or_404
from categories.models import Category
from account.models import User
from taggit.managers import TaggableManager

class Project(models.Model):
    project_title = models.CharField(max_length=100, help_text='Project title should not exceed 100 character.')
    project_category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    project_details = models.TextField(null=True)
    project_total_target = models.IntegerField(null=True)
    project_start_date = models.DateField(null=True, blank=True)
    project_end_date = models.DateField(null=True, blank=True) 
    project_tags = TaggableManager()
    project_created_date = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.project_title


class Image(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='project/imgs', null=True)
    
class ReviewRating(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    rating = models.FloatField()
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)