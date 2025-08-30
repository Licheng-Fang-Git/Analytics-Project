from django.db import models

# Create your models here.
class Followers(models.Model):
    date = models.DateField()
    follower_increase = models.IntegerField(null=True, blank=True)
    total_follower_count = models.IntegerField(null=True, blank=True)
    month_year = models.DateField()

    def __str__(self):
        return f"{self.date} - {self.total_follower_count}"