from django.db import models

# Create your models here.
class Post(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering=('name',)
        verbose_name_plural= 'Posts'

    def __str__(self):
        return self.name
