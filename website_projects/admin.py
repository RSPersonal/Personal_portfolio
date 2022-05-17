from django.contrib import admin
from .models import PropertyModel


# Register your models here.
class PropertiesAdmin(admin.ModelAdmin):
    standard_fields = ('city', 'municipality', 'street', 'housenumber')
    list_display = standard_fields
    search_fields = standard_fields


admin.site.register(PropertyModel, PropertiesAdmin)
