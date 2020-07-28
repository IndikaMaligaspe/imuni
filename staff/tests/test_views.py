from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User , Permission
from mixer.backend.django import mixer
from datetime import datetime
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware

import pytest

pytestmark = pytest.mark.django_db

# Create your tests here.

from .. import views
from .. import models
# from .. import forms
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
    
    def setup_request(self, request):
        """Annotate a request object with a session"""
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        """Annotate a request object with a messages"""
        middleware = MessageMiddleware()
        middleware.process_request(request)
        request.session.save()

class TestInstructorSetup(BaseTest):
    def test_index(self):
        instructor = mixer.blend(User, username='test-instructor', 
                            groups__name='Instructor')

        req = self.factory.get('/')
        self.setup_request(req)
        req.user = instructor
        resp = views.InstructorCreateOrUpdateAccount.as_view()(req)
        assert resp.status_code == 200, 'Can create instructor'
    
    def test_post_update(self):
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

        # instructor.profiles.add(profile)
        instructor.save()
        data = {
            'first_name': User.first_name,
            'last_name': User.last_name,
            'email': User.email,
            'email_display': instructor.profiles.email_display,
            'bio': 'The world and its environment has been going',
            'language': 'en',
            'phone': '1111',
            'mobile': '2222',
            'address': 'Test one two',
            'city': 'CMB',
            'country': 'LK'
        }
        url = reverse('instructor_update', kwargs={'staff_id':instructor.pk})
        req = self.factory.post(url, data=data)
        self.setup_request(req)
        req.user = instructor
        resp = views.InstructorCreateOrUpdateAccount.as_view()(req, staff_id=instructor.pk)
        assert resp.status_code != 405, 'Check logged in user tp update profile'
        assert 'saved sucess' in resp.content.decode(), 'Valid instructor can update profile'

