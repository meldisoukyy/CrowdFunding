from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Sum
# Create your models here.

class Donation(models.Model):
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE,related_name='donations')
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.amount)

    @classmethod
    def totalDonation(cls,project):
        sum = Donation.objects.filter(project=project).aggregate(total=Sum('amount'))
        if not sum['total']:
            return 0

        return sum['total']
