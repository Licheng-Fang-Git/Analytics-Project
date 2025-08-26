from django.db import models

# Create your models here.


class LinkedInPost(models.Model):
    day_of_week = models.CharField(max_length=20)
    impressions = models.IntegerField()
    clicks = models.IntegerField(null=True, blank=True)
    likes = models.IntegerField(null=True, blank=True)
    comments = models.IntegerField(null=True, blank=True)
    shares = models.IntegerField(null=True, blank=True)
    post_type = models.CharField(max_length=50, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    sub_category = models.CharField(max_length=100, null=True, blank=True)
    engagement_rate = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.day_of_week} - {self.impressions}"