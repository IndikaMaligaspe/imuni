from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView 
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CourseEnrolmentForm
from courses.models import  Course, Module 
from cart.cart import Cart
class StudentRegistrationView(CreateView):
    template_name = 'students/student/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('student_course_list')

    def form_valid(self,request, form):
        result = super(StudentRegistrationView, 
                       self).form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'],
                            password=cd['password1'])
        login(self, request, user)
        return result

class StudentEnrollCourseView(LoginRequiredMixin, View):

    def post(self,request):
        cart = Cart(request)
        student = self.request.user
        countries = {'LK':'Sri Lanka', 'IN':'Inidia','US':'United States','CA':'Canada'}
        print(student)
        return render(request,'students/course/enrol.html',{'cart':cart, 
                                                            'student':student,
                                                            'countries':countries})
        
     

class StudentCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'students/course/list.html'

    def get_queryset(self):
        qs = super(StudentCourseListView, self).get_queryset()
        qs = qs.filter(students__in=[self.request.user])
        # print(len(qs))
        return qs 

class StudentCourseDetailView(DetailView):
    model = Course
    template_name = Coursetemplate_name = 'students/course/detail.html'

    def get_queryset(self):
        qs = super(StudentCourseDetailView, self).get_queryset()
        qs = qs.filter(students__in=[self.request.user])
        # print(len(qs))
        return qs
    
     
    def get_context_data(self, **kwargs):
        context = super(StudentCourseDetailView, self).get_context_data(**kwargs)
        course = self.get_object()
        # print(course.modules.filter(id = 9).first())
        if 'module_id' in self.kwargs:
            module = course.modules.filter(id = self.kwargs['module_id']).first()
            context['module'] = module
        else:
            context['module'] = course.modules.all().first()
        return context
    
