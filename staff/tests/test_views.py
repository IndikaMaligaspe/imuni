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
        # print(req.user.first_name)
        resp = views.InstructorCreateAccount.as_view()(req)
        assert resp.status_code == 200, 'Can create instructor'