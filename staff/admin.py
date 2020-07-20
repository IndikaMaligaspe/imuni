from django.contrib import admin
from .models import Profiles
# Register your models here.

@admin.register(Profiles)
class ProfileAdmin(admin.ModelAdmin):
    list_display =['user','bio','photo','webpage']