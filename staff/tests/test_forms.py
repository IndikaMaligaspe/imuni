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


class TestProfilesForm(BaseTest):
    def test_get_form(self):
        profile_form = forms.ProfileForm()
        assert 'country' in profile_form.fields, 'Can load profile form' 