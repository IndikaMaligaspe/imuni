from django import forms
from django.forms.models import inlineformset_factory
from django.forms import TextInput, Textarea
from .models import Course, Module

ModuleFormSet = inlineformset_factory(Course, Module, 
                                    fields=['title', 'description', 'duration'],
                                    widgets={'title':TextInput(attrs={'size':'50'}), \
                                            'duration': TextInput(attrs={'size':'3'}),\
                                            'description': Textarea(attrs={'rows':'5' , 'cols':'83'})},
                                    extra=3, can_delete=True)

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title', 'slug', 'subject', 'overview', 'requirements', 'content_summary', 'thumbnail_image', 'duration', 'level', 'price', 'language')
