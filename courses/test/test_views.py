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

from .. import views
from .. import models
from .. import forms

class BaseTest(TestCase):
    client = Client()
    def setUp(self):
        super(BaseTest, self).setUp()

        self.instructor = {
            'name': 'Jonthan',
            'username': 'JonthanM',
            'password':'rezgate123@#'
        }
        models.Subject.objects.create(title='Software Engineering', slug='software-engineer', language='en', client_id=0)
        self.subject = models.Subject.objects.get(pk=1)
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
        # req = RequestFactory()
        req = self.factory.get('/')
        self.setup_request(req)
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
        # req = RequestFactory().get('/')
        req = self.factory.get('/')
        self.setup_request(req)
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
        # req = RequestFactory()
        req = self.factory.get('/')
        self.setup_request(req)
        req.user = course.owner
        resp = views.InstructorCourseView.as_view()(req)
        output = str(resp.content.decode())
        assert resp.status_code == 200
        assert course.title in output, 'courses for instrutuctor should be available'
        assert owner.first_name in output, 'Instructor details are available in output'
        # self.assertContains(resp, owner.first_name, msg_prefix='Instructor details are available in output')

class TestCourseCreateView(BaseTest):
    """
      Test create Course view actions
    """

    def test_loadform(self):
        instructor = mixer.blend(User, username='test-instructor', password='abcd1234',
                            groups__name='Instructor')
        perm = Permission.objects.get(codename='add_course')
        instructor.user_permissions.add(perm)  
        instructor.save()                  
        # req = RequestFactory().get('/')
        url = reverse('course_create')
        print(f'URL-------------{url}')  
        req = self.factory.get(url)
        self.setup_request(req)
        req.user = instructor
        resp = views.CourseCreateView.as_view()(req)
        output = str(resp.content.decode())
        # print(output)
        assert resp.status_code == 200, 'instructor with permission can login'
        assert 'overview' in output, 'create form available for instrtuctor'
    
    def test_course_create_with_empty(self):
        data = {
        }
        instructor = mixer.blend(User, username='test-instructor', password='abcd1234',
                            groups__name='Instructor')
        perm = Permission.objects.get(codename='add_course')
        instructor.user_permissions.add(perm)
        instructor.save()                  
        # req = RequestFactory().post('/', data=data)
        url = reverse('course_create')  
        req = self.factory.post(url, data=data)
        self.setup_request(req)
        req.user = instructor
        resp = views.CourseCreateView.as_view()(req)
        output = str(resp.content.decode())
        # print(output)
        assert resp.status_code == 200, 'instructor can submit course form'
        assert 'failed' in output, 'course created for instrtuctor'

    def test_course_create_with_data(self):
        data = {
           'title': 'test title',
           'slug': 'test-title',
           'subject':self.subject.pk,
           'overview' : 'thsi is a test creation',
           'requirements': 'need to be fit',
           'content_summary': 'testing your fitness',
           'thumbnail_image': '',
           'duration': '5',
           'level': 'Beginner',
           'price': 35,
           'language': 'en'
        }
        instructor = mixer.blend(User, username='test-instructor', password='abcd1234',
                            groups__name='Instructor')
        perm = Permission.objects.get(codename='add_course')
        instructor.user_permissions.add(perm)
        instructor.save()           
        url = reverse('course_create')      
        print(f'URL-------------{url}')   
        req = self.factory.post(url, data=data)
        self.setup_request(req)
        req.user = instructor
        resp = views.CourseCreateView.as_view()(req)
        output = str(resp.content.decode())
        # print(output)
        assert resp.status_code == 200, 'instructor can submit course form'
        assert 'saved' in output, 'course created for instrtuctor'

class TestCourseUpdateView(BaseTest):

    def test_course_update_get_form(self):
        instructor = mixer.blend(User, username='test-instructor', password='abcd1234',
                            groups__name='Instructor')
        perm = Permission.objects.get(codename='change_course')
        instructor.user_permissions.add(perm)
        instructor.save()                  
        course = mixer.blend(models.Course)
        url = reverse('course_edit', kwargs={'pk':4})
        req = self.factory.get(url)
        self.setup_request(req)
        req.user = instructor
        resp = views.CourseUpdateView.as_view()(req, pk=course.pk)
        output = str(resp.content.decode())
        assert resp.status_code == 200, 'Instructor can get form'
        assert course.title in output, 'Instructor should get retrieved course'


    def test_course_update_post_data(self):
        instructor = mixer.blend(User, username='test-instructor', password='abcd1234',
                            groups__name='Instructor')
        perm = Permission.objects.get(codename='change_course')
        instructor.user_permissions.add(perm)
        instructor.save()
        course = mixer.blend(models.Course)
        data = {
           'title': 'test title',
           'slug': 'test-title',
           'subject':self.subject.pk,
           'overview' : course.overview,
           'requirements': course.requirements,
           'content_summary': course.content_summary,
           'thumbnail_image': course.thumbnail_image,
           'duration': course.duration,
           'level': course.level,
           'price': 35,
           'language': course.language
        }
        url = reverse('course_edit', kwargs={'pk':4})
        req = self.factory.post(url, data=data)
        self.setup_request(req)
        req.user = instructor
        resp = views.CourseUpdateView.as_view()(req, pk=course.pk)
        assert resp.status_code == 200, 'Instructor should be able to update course' 
        course.refresh_from_db()
        assert course.title == 'test title', 'Instructor saved data'

class TestCourseDeleteVoew(BaseTest):
    def test_delete_view_load_page(self):
        instructor = mixer.blend(User, username='test-instructor', password='abcd1234',
                            groups__name='Instructor')
        perm = Permission.objects.get(codename='delete_course')
        instructor.user_permissions.add(perm)
        instructor.save()
        course = mixer.blend(models.Course)
        req = self.factory.get('/')
        self.setup_request(req)
        req.user = instructor
        resp = views.CourseDeleteView.as_view()(req, pk=course.pk)
        assert resp.status_code == 200, 'Instructor should be able to get delete confirmation page' 

    def test_delete_course_with_valid_data(self):
        instructor = mixer.blend(User, username='test-instructor', password='abcd1234',
                            groups__name='Instructor')
        perm = Permission.objects.get(codename='delete_course')
        instructor.user_permissions.add(perm)
        instructor.save()
        course = mixer.blend(models.Course)
        req = self.factory.post('/')
        self.setup_request(req)
        req.user = instructor
        resp = views.CourseDeleteView.as_view()(req, pk=course.pk)
        assert resp.status_code == 200, 'Instructor should be able to delete course' 
        try:
            course.refresh_from_db()
            assert False
        except Exception as a:
            assert str(a) == 'Course matching query does not exist.', 'Instructor deleted course'


class TestCourseModuleUpdateView(BaseTest):
    def test_load_course_modules(self):
        instructor = mixer.blend(User, username='test-instructor', password='abcd1234',
                            groups__name='Instructor')
        perm = Permission.objects.get(codename='delete_course')
        instructor.user_permissions.add(perm)
        instructor.save()
        course = mixer.blend(models.Course, client_id=0, language='en', owner=instructor) 
        obj = mixer.cycle(4).blend('courses.Module',
                          course=course,
                          title='SE',
                          description='This module is for SE',
                          order=mixer.sequence(lambda c: c),
                          language='en',
                          client_id=0)       
        req =  self.factory.get('/')
        self.setup_request(req)
        req.user = instructor
        resp = views.CourseModuleUpdateView.as_view()(req, pk=course.pk)
        assert resp.status_code == 200, 'instructor can view course modules to edit / add' 

    def test_update_course_module(self):
        instructor = mixer.blend(User, username='test-instructor', password='abcd1234',
                            groups__name='Instructor')
        perm = Permission.objects.get(codename='delete_course')
        instructor.user_permissions.add(perm)
        instructor.save()
        course = mixer.blend(models.Course, client_id=0, language='en', owner=instructor) 
        obj = mixer.cycle(1).blend('courses.Module',
                          course=course,
                          title='SE',
                          description='This module is for SE',
                          order=mixer.sequence(lambda c: c),
                          language='en',
                          client_id=0)   
        data = {
            'modules-TOTAL_FORMS': '2',
            'modules-INITIAL_FORMS': '0',
            'modules-MAX_NUM_FORMS': '100',
            'id_modules-0-title':'Python For All',
            'id_modules-0-description': 'Lets learn python the right way',
            'id_modules-0-duration': 'Lets learn python the right way',
            'id_modules-0-DELETE':'no',
            'id_modules-1-title':'Python For All',
            'id_modules-1-description': 'Lets learn python the right way',
            'id_modules-1-duration': 'Lets learn python the right way',
            'id_modules-1-DELETE':'no',
        }                  
        url = reverse('course_module_update', kwargs={'pk':4})    
        req =  self.factory.post(url,data=data)
        self.setup_request(req)
        req.user = instructor
        resp = views.CourseModuleUpdateView.as_view()(req, pk=course.pk)
        assert resp.status_code == 200, 'instructor can add moduls'