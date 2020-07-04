from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User , Permission
from mixer.backend.django import mixer
from datetime import datetime
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user
import pytest

pytestmark = pytest.mark.django_db


from .. import forms
from .. import models

class BaseTest(TestCase):
    def setUp(self):
        models.Subject.objects.create(title='Software Engineering', slug='software-engineer', language='en', client_id=0)
        self.subject = models.Subject.objects.get(pk=1)

class TestCourseForm(BaseTest):
    def test_form_with_empty_data(self):
        form = forms.CourseForm(data={})
        assert form.is_valid() is False, 'Should be invalid if no data'

    def test_form_with_valid_data(self):
        data = {    
           'title': 'test title',
           'slug': 'test-title',
           'subject': self.subject.pk,
           'overview' : 'thsi is a test creation',
           'requirements': 'need to be fit',
           'content_summary': 'testing your fitness',
           'thumbnail_image': '',
           'duration': '5',
           'level': 'Beginner',
           'price': 35,
           'language': 'en'
        }
        form = forms.CourseForm(data)
        valid = form.is_valid()
        assert valid is True, 'Should be validated with right data'
        

