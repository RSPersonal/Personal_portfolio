from django.db import models


# Create your models here.
class VisitorCount(models.Model):
    visitor_count = models.IntegerField(default=1)


class ProfilePosts(models.Model):
    post = models.TextField()
    order = models.IntegerField(default=1)
    language = models.CharField(default='EN', max_length=10)

    def __str__(self):
        return self.post


class VersionHistory(models.Model):
    version_number = models.CharField(max_length=40, default='')

    def __str__(self):
        return self.version_number
