import pytest
from mixer.backend.django import mixer
from django.contrib.auth.models import AnonymousUser, User, Group
from datetime import datetime
pytestmark = pytest.mark.django_db


class TestCourse:
    def test_model_create(self):
        owner = mixer.blend(User, username='test-instructor', 
                            groups__name='Instructor')
        student = mixer.blend(User, username='test-student', 
                            groups__name='Student')
        obj = mixer.blend('courses.Course',  
                          owner=owner,
                          slug='test-course', 
                          overview='This is a test a course', 
                          requirement='test requirement', 
                          content_summary='test_summary', 
                          created=datetime.now(),
                          student=student,
                          duration=10.5, 
                          language='en', 
                          client_id=1)
        assert obj.pk == 1, 'Should be able to create Course instance'
    
class TestModule:
    def test_model_create(self):
        course = mixer.blend('courses.Course')
        obj = mixer.cycle(4).blend('courses.Module',
                          course=course,
                          title='SE',
                          description='This module is for SE',
                          order=mixer.sequence(lambda c: c),
                          language='en',
                          client_id=1)
        assert obj[0].pk == 1, 'Should be able to create Modules'