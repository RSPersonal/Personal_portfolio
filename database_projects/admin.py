from django.contrib import admin
from .models import Portfolio, Positions, MotivationLetter


# Register your models here.
class PortfolioAdmin(admin.ModelAdmin):
    pass


class MotivationLetterAdmin(admin.ModelAdmin):
    pass


admin.site.register(MotivationLetter, MotivationLetterAdmin)
admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(Positions, PortfolioAdmin)
