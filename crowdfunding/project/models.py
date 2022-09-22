from distutils.command import upload
from django.db import models
from django.shortcuts import get_list_or_404
from categories.models import Category
from account.models import User
from donation.models import Donation
from taggit.managers import TaggableManager
from django.db.models import Sum, Count


class Project(models.Model):
    project_title = models.CharField(
        max_length=100, help_text='Project title should not exceed 100 character.')
    project_category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True)
    project_details = models.TextField(null=True)
    project_total_target = models.IntegerField(null=True)
    project_start_date = models.DateField(null=True, blank=True)
    project_end_date = models.DateField(null=True, blank=True)
    project_tags = TaggableManager()
    project_main_image = models.ImageField(upload_to='project/imgs', null=True)
    is_featured = models.BooleanField(default=False, null=True)
    project_created_date = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.project_title

    def totalDonation(self):
        sum = Donation.objects.filter(
            project=self).aggregate(total=Sum('amount'))
        if not sum['total']:
            return 0
        return sum['total']

    def allDonations(self):
        return Donation.objects.filter(project=self)

    def deleteOrNot(self):
        if (int(self.totalDonation()) / int(self.project_total_target)) * 100 > 25:
            return False

        return True

    def donation_ratio(self):
        return (int(self.totalDonation()) / int(self.project_total_target)) * 100

    def averageReview(self):
        total_reviews = ReviewRating.objects.filter(
            project=self).aggregate(total=Sum('rating'))
        number_of_people = ReviewRating.objects.filter(
            project=self).aggregate(total=Count('project'))
        if number_of_people['total'] == 0 or total_reviews['total'] == 0:
            return 0
        return total_reviews['total'] / number_of_people['total']


class Image(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='project/imgs', null=True)


class ReviewRating(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    rating = models.FloatField()
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
