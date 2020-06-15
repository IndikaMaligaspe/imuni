from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.forms.models import modelform_factory
from django.apps import apps
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.db.models import Count, Avg
from .models import Course, Content, Module, Subject, Profiles, InstructorRating, CourseRating
from .forms import ModuleFormSet
# from students.forms import CourseEnrolmentForm 
from django.db.models import Q
import json


# class ManageCourseListView(ListView):
    # model = Course
    # template_name = "course/manage/course/list.html"
    
    # def get_queryset(self):
    #     queryset = super(ManageCourseListView, self).get_queryset()
    #     queryset = queryset.filter(owner=self.request.user)
    #     return queryset

class OwnerMixin(object):

    def get_queryset(self):
        queryset = super(OwnerMixin, self).get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset

class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(OwnerEditMixin, self).form_valid(form)

class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin):
    model = Course

    fields = ['subject','title','slug','overview']
    success_url = reverse_lazy('manage_courses_list')

class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    fields = ['subject', 'title', 'slug','overview']
    success_url = reverse_lazy('manage_course_list')
    template_name = 'courses/manage/course/form.html'

class ManageCourseListView(OwnerCourseMixin, ListView):
     template_name = "courses/manage/course/list.html"

class CourseCreateView(PermissionRequiredMixin, OwnerCourseEditMixin, CreateView):
    permission_required = 'courses.add_courses'

class CourseUpdateView(PermissionRequiredMixin, OwnerCourseEditMixin, UpdateView):
    permission_required = 'courses.change_course'


class CourseDeleteView(PermissionRequiredMixin, OwnerCourseEditMixin,DeleteView):
    template_name = 'courses/manage/course/delete.html' 
    success_url = reverse_lazy('manage_course_list')
    # permission_required = 'courses.delete_coursecourse_module_update'

class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/formset.html'
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)
    
    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course,
                                id=pk,
                                owner=request.user)
        return super(CourseModuleUpdateView, self).dispatch(request, pk)
    
    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course, 
                                       'formset':formset})
    
    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({'course': self.course, 
                                        'formset': formset})

class ContentCreatUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'

    def get_model(self, model_name):
        if model_name in ['text','video', 'image', 'file']:
            return apps.get_model(app_label='courses', model_name = model_name)
        return None
    
    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude = ['owner','order', 'created','updated'])
        return Form(*args, ** kwargs)
        
    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(Module, id=module_id, course__owner = request.user)
        self.model= self.get_model(model_name)
        if id:
            self.obj=get_object_or_404(self.model, id=id, owner=request.user)
        return super(ContentCreatUpdateView, self).dispatch(request, module_id, model_name, id)
    
    def get(self, request, module_id, model_name, id=None):
        form= self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form':form, 'object':self.obj})
    
    
    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, 
                            instance=self.obj,
                            data=request.POST, 
                            files = request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                Content.objects.create(module=self.module, item=obj)
            return redirect('module_content_list', self.module.id)
        return self.render_to_response({'form':form, 'object':self.obj})

class ContentDeleteView(View):
    def post(self, request, id):
        content = get_object_or_404(Content, id=id, module__course__owner =reqeust_user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('module_content_list', module.id)

class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module, 
                                  id = module_id, 
                                  course__owner = request.user)
        return self.render_to_response({'module':module})


class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(id = id, course__owner=request.user).update(order=order)
        return self.render_json_response({'saved':'OK'})
    

class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id , order in self.request_json.items():
            Content.objects.filter(id = id, module__course__owner=request.user).update(order=order)
        return self.render_json_reponse({'saved':'OK'})


class CourseListView(TemplateResponseMixin, View):
    model = Course
    template_name = 'home.html'

    def get(self, request, subject=None):
        subjects = Subject.objects.annotate(total_courses=Count('courses'))[:5]
        courses = Course.objects.annotate(total_modules = Count('modules'))[:12]
        instructors =  query = Course.objects.values('owner__id').annotate(count=Count('owner_id')).values('owner__first_name','owner__last_name', 'owner__profiles__bio','owner__profiles__photo','count').order_by('-count')[:5]
        students_review = User.objects.filter(groups=4).values('first_name','last_name','profiles__photo')[:6]
    
        if subject:
            subject = get_object_or_404(Subject,slug=subject)
            courses = courses.filter(subject=subject)
        return self.render_to_response({'subjects': subjects, 
                                         'subject':subject,
                                         'courses':courses,
                                         'instructors':instructors,
                                         'students_review':students_review})



class CourseDetailView(DetailView):
    model  =  Course
    template_name = "courses/course/detail.html"
    
    def get(self, request, slug):
        course = get_object_or_404(Course, slug=slug)
        instructor_ratings = InstructorRating.objects.annotate(avg_rating = Avg('rating')).annotate(review_count = Count('review')).annotate(students=Count('instructor__courses_created__students')).annotate(course_count = Count('instructor__courses_created', distinct=True)).filter(instructor = course.owner)
        course_avg_ratings = CourseRating.objects.all().filter(course=course.id).aggregate(Avg('rating')) 
        course_wise_ratings = CourseRating.objects.values('rating').filter(course=4).annotate(rate_count = Count('rating')).values('rating','rate_count').order_by()
        print(course.id)
        print(course_avg_ratings['rating__avg'])
        return self.render_to_response({'course':course,
                                         'instructor_ratings':instructor_ratings,
                                         'course_avg_ratings':course_avg_ratings,
                                         'course_wise_ratings':course_wise_ratings})


    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrolmentForm(initial={'course':self.object})
        return context
    

class SearchMain(TemplateResponseMixin, View):
    template_name = "search_main.html"
    
    def get(self, request):
        search_term =request.GET.get('search_term')
        skill_filter = request.GET.get('hid_skill_filter')
        paid_filter  = request.GET.get('hid_paid_filter')
        hid_rating_filter =request.GET.get('hid_ratind_filter') 
        
        hid_skill_filter = {
                'All Levels':'0',
                'Beginner':'0',
                'Intermediate':'0',
                'Advance':'0',
        }

        hid_paid_filter = {
                'Free':'0',
                'Paid':'0',
        }
 
        qry_skill_filter   = []
        qry_paid_filter = []
        qry_paid_filter


        if skill_filter:
            for skill in skill_filter.split(","):
                if skill:
                    hid_skill_filter[skill] = '1'
                    qry_skill_filter.append(skill)
        else:
            qry_skill_filter.extend(["All Levels","Beginner","Intermediate","Advance"])       

        
        if paid_filter:
            for filter_item in paid_filter.split(","):
                if filter_item:
                    hid_paid_filter[filter_item]  = '1'
                    qry_paid_filter.append(filter_item)
        else:
            qry_paid_filter.extend(["Paid","Free"])

        print('---------{}  - {}  -  {}'.format(qry_paid_filter,qry_skill_filter,hid_rating_filter))
        # print(paid_filter)
        courses = Course.objects.filter(Q(title__icontains=search_term)| Q(owner__first_name__icontains=search_term)).filter(level__in=qry_skill_filter).annotate(average_rating=Avg('course_review__rating')).values('title','slug', 'thumbnail_image','overview','duration','price','level','owner__first_name','owner__last_name').annotate(avg_rating=Avg('course_review__rating'))
        
        if hid_rating_filter:
            courses = courses.filter(avg_rating__gte = hid_rating_filter)
        # print(hid_skill_filter);
        return self.render_to_response({'result_courses':courses,
                                         'search_term':search_term,
                                         'hid_paid_filter':hid_paid_filter,
                                         'hid_skill_filter': hid_skill_filter,
                                         'hid_rating_filter' : hid_rating_filter})