from django import forms
from courses.models import Course

class CourseEnrolmentForm(forms.Form):
    """CourseEnrolmentForm definition."""
    course = forms.ModelChoiceField(queryset=Course.objects.all(),
                                     widget=forms.HiddenInput)
 

