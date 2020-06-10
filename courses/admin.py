from django.contrib import admin
from .models import Subject, Course, Module, Profiles, Content, CourseRating, SiteReview
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


User = get_user_model()


# Register your models here.


@admin.register(Subject)
class SubjectAdmin (admin.ModelAdmin):
    list_dislplay = ['title','slug']
    prepoulated_fields = {'slug': ('title',)}

class ModuleInline(admin.StackedInline):
    model = Module

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
   list_display = ['title','subject','created']
   list_filter = ['created','subject']
   search_filter = ['title', 'overview'] 
   prepopulated_fields = {'slug': ('title',)}
   inlines = [ModuleInline]

@admin.register(Profiles)
class ProfileAdmin(admin.ModelAdmin):
    list_display =['user','bio','photo']


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    model = Content

@admin.register(CourseRating)
class CourseRatingAdmin(admin.ModelAdmin):
    model = CourseRating

@admin.register(SiteReview)
class SiteReviewAdmin(admin.ModelAdmin):
    model = SiteReview