from django.db import models


# Create your models here.
class PropertyModel(models.Model):
    street = models.CharField(max_length=50, blank=True, null=True)
    housenumber = models.IntegerField(blank=True, null=True)
    housenumber_add = models.CharField(max_length=15,blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    municipality = models.CharField(max_length=60, blank=True, null=True)
    province = models.CharField(max_length=60, blank=True, null=True)
    ask_price = models.IntegerField()
    construction_year = models.IntegerField(blank=True, null=True)
    amount_rooms = models.IntegerField(default=0, null=True)
    description = models.TextField(blank=True, null=True)
    thumbnail_photo = models.ImageField(upload_to='images/', blank=True, null=True)
    other_photos = models.ImageField(blank=True,null=True)
    added_on = models.DateTimeField(auto_now=True)

    def remove_on_image_update(self):
        try:
            obj = PropertyModel.objects.get(id=self.id)
        except PropertyModel.DoesNotExist:
            return

        if obj.thumbnail_photo and self.thumbnail_photo and obj.thumbnail_photo != self.image:
            obj.thumbnail_photo.delete()
        elif obj.other_photos and self.other_photos and obj.other_photos != self.other_photos:
            obj.thumbnail_photo.delete()

    def safe(self, *args, **kwargs):
        self.remove_on_image_update()
        return super(PropertyModel, self).save(*args, **kwargs)
