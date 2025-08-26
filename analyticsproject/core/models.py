from django.db import models

# Create your models here.


class LinkedInPost(models.Model):
    post_title = models.TextField(null=True, blank=True)
    post_link = models.URLField(unique=True)
    created_date = models.DateField()
    impressions = models.IntegerField(null=True, blank=True)
    clicks = models.IntegerField(null=True, blank=True)
    ctr = models.FloatField(null=True, blank=True)
    likes = models.IntegerField(null=True, blank=True)
    comments = models.IntegerField(null=True, blank=True)
    engagement_rate = models.FloatField(null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    sub_category = models.CharField(max_length=100, null=True, blank=True)
    year = models.IntegerField()
    month = models.CharField(max_length=20)
    day_of_week = models.CharField(max_length=20)
    time_of_posting = models.TimeField()
    emoji = models.BooleanField(default=False)
    type_of_post = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return f"{self.post_title or 'Untitled'}, {self.impressions}"