from django.db import models

# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=350)
    description = models.TextField(default="")
    completed = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title