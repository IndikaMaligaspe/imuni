from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User , Permission
from mixer.backend.django import mixer
from datetime import datetime
from django.test import Client
from django.contrib.auth import get_user

import pytest

pytestmark = pytest.mark.django_db

from .. import models
from home.models import Countries

class BaseTest(TestCase):
    client = Client()
    def setUp(self):
        super(BaseTest, self).setUp()

        self.instructor = {
            'name': 'Jonthan',
            'username': 'JonthanM',
            'password':'rezgate123@#'
        }
        self.factory = RequestFactory()
    

class TestInstructor(BaseTest):
    def test_instructor_create(self):
        instructor = mixer.blend(User, username='test-instructor',
                                first_name='JJJ',last_name='Martin',
                                email='jj@martin.com',
                                groups__name='Instructor')
        # instructor = models.Instructor()

        new_instructor = User.objects.get(pk=instructor.id)
        assert new_instructor.username == instructor.username, "Instructor can be created"

    def test_instructor_create_profile(self):
        instructor = mixer.blend(User, username='test-instructor',
                                first_name='JJJ',last_name='Martin',
                                email='jj@martin.com',
                                groups__name='Instructor')
        country = mixer.blend(Countries,country_code='SL',country_name='Sri Lanka')                        
        profile = mixer.blend(models.Profiles, user=instructor, 
                              bio='test bio for JJ', photo=None,
                              city='Colombo', country=country,
                              email_display='0',webpage='www.iceman.com',
                              phone='9999 0226', mobile= '0414 991 9921',
                              address='No. 04, Geethanjalee place, colombo 04',
                              language='en', client_id=0)
    

        new_instructor = User.objects.get(pk=instructor.id)
        assert new_instructor.profiles.bio == 'test bio for JJ', 'Instructor can create profiles'
        assert new_instructor.profiles.phone == '9999 0226', 'Instructor personal information can be created'
