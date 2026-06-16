from django.contrib import admin
from .models import Profile, PortfolioImage

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','role','domain','name')

@admin.register(PortfolioImage)
class PortfolioImageAdmin(admin.ModelAdmin):
    list_display = ('profile','caption','uploaded_at')
