from django.db import models

# Create your models here.
class LifeEvent(models.Model):
    title = models.TextField(max_length=50)
    description = models.TextField()
    created_on = models.DateTimeField()