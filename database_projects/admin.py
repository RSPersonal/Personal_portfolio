from django.contrib import admin
from .models import Portfolio, Positions


# Register your models here.
class PortfolioAdmin(admin.ModelAdmin):
    pass


admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(Positions, PortfolioAdmin)
