from django.test import RequestFactory, TestCase
from django.contrib.auth.models import AnonymousUser, User, Group
from mixer.backend.django import mixer
from datetime import datetime
from django.test import Client
from django.urls import reverse
import pytest

pytestmark = pytest.mark.django_db

from .. import views
from .. import models

class BaseTest(TestCase):
    client = Client()
    def setUp(self):
        super(BaseTest, self).setUp()


class TestInstructorCourseView(BaseTest):
    def test_get_courses_by_instructor(self):
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


        # instructor = mixer.blend(User, 
        #                    username='test-instructor', 
        #                    groups__name='Instructor')
        req = RequestFactory().get('/')
        req.user = owner
        # print(req.user.first_name)
        resp = views.InstructorCourseView.as_view()(req)
        assert resp.status_code == 200, "Instructor can access."
        assert req.user.first_name in resp.content.decode(), "Instructor should get a course list" 

class TestManageCourseListView(BaseTest):
    """ 
    test aManageCourseList for valid users to add / edit / 
    remove courses assigned to them
    """   
    def test_test_manage_course_list_instructor_avaialbility(self):
        owner = mixer.blend(User, username='test-instructor', 
                            groups__name='Instructor')
        req = RequestFactory().get('/')
        req.user = owner
        # print(req.user.first_name)
        resp = views.InstructorCourseView.as_view()(req)
        assert resp.status_code == 200, "Logged in instructor can acccess."

    def test_instructotr_get_list_of_courses(self):
        owner = mixer.blend(User, username='test-instructor', password='abcd1234',
                            groups__name='Instructor')
        student = mixer.blend(User, username='test-student', 
                            groups__name='Student')
        course = mixer.blend('courses.Course',  
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
        req = RequestFactory().get('/')
        req.user = course.owner
        resp = views.InstructorCourseView.as_view()(req)
        output = str(resp.content.decode())
        assert resp.status_code == 200
        assert course.title in output, 'courses for instrutuctor should be available'
        assert owner.first_name in output, 'Instructor details are available in output'
        # self.assertContains(resp, owner.first_name, msg_prefix='Instructor details are available in output')

        