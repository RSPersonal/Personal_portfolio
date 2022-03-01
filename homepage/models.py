from django.db import models


# Create your models here.
class VisitorCount(models.Model):
    visitor_count = models.IntegerField()


class ProfilePosts(models.Model):
    post = models.TextField()
    order = models.IntegerField(default=1)

    def __str__(self):
        return self.post
