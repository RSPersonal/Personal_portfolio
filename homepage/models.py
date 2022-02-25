from django.db import models


# Create your models here.
class VisitorCount(models.Model):
    visitor_count = models.IntegerField()

