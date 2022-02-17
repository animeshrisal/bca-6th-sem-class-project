from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=100)
    budget = models.BigIntegerField(blank=True, null=True)
    genres = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title