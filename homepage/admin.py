from django.contrib import admin
from .models import ProfilePosts


# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(ProfilePosts, ProfileAdmin)
