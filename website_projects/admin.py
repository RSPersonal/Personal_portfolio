from django.contrib import admin
from .models import PropertyModel


# Register your models here.
class PropertiesAdmin(admin.ModelAdmin):
    pass


admin.site.register(PropertyModel, PropertiesAdmin)