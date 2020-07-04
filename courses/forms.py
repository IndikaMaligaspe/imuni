from django import forms
from django.forms.models import inlineformset_factory
from .models import Course, Module

ModuleFormSet = inlineformset_factory(Course, Module, 
                                    fields=['title', 'description'], 
                                    extra=2, can_delete=True)

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title', 'slug', 'subject','overview', 'requirements', 'content_summary', 'thumbnail_image', 'duration', 'level', 'price', 'language')
