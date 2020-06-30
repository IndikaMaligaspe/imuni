from django.test import RequestFactory, TestCase
from django.contrib.auth.models import AnonymousUser, User, Group
from mixer.backend.django import mixer
import pytest

pytestmark = pytest.mark.django_db

from .. import views

class TestLoggedInView(TestCase):
    def test_loggedIn_instructor(self):
        user = mixer.blend(User, username='test-instructor', groups__name='Instructor')
        req = RequestFactory().get('/')
        req.user = user
        resp = views.LoggedInView.as_view()(req)
        # print(resp._headers)
        assert resp.status_code == 200, "Authenticated users can access"
        assert 'instructor_dashboard.html' in resp.get('Response-URL'), "Authenticated instructur should go to instructor_dashboard "


    def test_loggedIn_lecturer(self):
        user  = mixer.blend(User, username='test_lecturer', groups__name='Lecturer')
        req = RequestFactory().get("/")
        req.user = user
        resp = views.LoggedInView.as_view()(req)
        assert resp.status_code == 200, "Authenticated lecturer can access"
        assert 'lecturer_dashboard.html' in resp.get('Response-Url'), "Authenticated Lecturer should go to lecturere dashboard"

    def test_loggedIn_lecturer(self):
        user  = mixer.blend(User, username='test_lecturer', groups__name='Student')
        req = RequestFactory().get("/")
        req.user = user
        resp = views.LoggedInView.as_view()(req)
        assert resp.status_code == 200, "Authenticated student can access"
        assert 'student_dashboard.html' in resp.get('Response-Url'), "Authenticated Student should go to lecturere dashboard"

    def test_loggedIn_anonymouss(self):
        req = RequestFactory().get("/")
        req.user = AnonymousUser()
        resp = views.LoggedInView.as_view()(req)
        assert resp.status_code == 302, "Authenticated anonymous can go to home"