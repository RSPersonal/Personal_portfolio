from django.contrib import admin
from .models import LifeEvent

# Register your models here.
class LifeEventAdmin(admin.ModelAdmin):
    pass

admin.site.register(LifeEvent, LifeEventAdmin)