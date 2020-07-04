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
from django.db.models import Q
from django.db.models.functions import Round
from django.utils.translation import get_language
from django.contrib import messages
import json
import logging

from courses.models import Course, Content, Module, Subject, Profiles, InstructorRating, CourseRating
from .forms import ModuleFormSet, CourseForm
from cart.forms import CartAddForm
from cart.cart import Cart
from common.functions import Admin as admin

from django.utils.translation import gettext_lazy as _


logger = logging.getLogger(__name__)

current_language = get_language()
print(f'language --- {current_language}')
class OwnerMixin(object):

    def get_queryset(self, request):
        client_id = admin.get_client_id('website', request)
        logger.info(f'queryset : OwnerMixin : {client_id} : {current_language} ')
        queryset = super(OwnerMixin, self).get_queryset(request)
        queryset = queryset.filter(owner=self.request.user).filter(client_id=client_id).filter(language=current_language)
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

class ManageCourseListView(LoginRequiredMixin, View):
     template_name = "courses/manage/course/list.html"
     
     def get(self, request, *args, ** kwargs):
         print(f'user --- {request.user}')
         queryset = Course.objects.filter(owner=request.user)
         return render(request, self.template_name, {'course_list':queryset})

class CourseCreateView(PermissionRequiredMixin, View):
    permission_required = 'courses.add_course'

    def get(self, request, *args, **kwargs):

        form = CourseForm()
        return render(request, 'courses/manage/course/form.html', {'action':'create','form':form, 'pk':'0'})
    
    def post(self, request, *args, **kwargs):
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.owner = request.user
            course.save()
            messages.success(request, "Course Created Succesfully")
            return render(request, 'courses/manage/course/form.html', {'action':'create','form':form, 'status':'saved', 'pk':course.pk})
        
        return (render(request, 'courses/manage/course/form.html', {'action':'create','status':'failed', 'pk':'0'}))

class CourseUpdateView(PermissionRequiredMixin, View):
    permission_required = 'courses.change_course'

    def get(self, request, *args, **kwargs):
        course = Course.objects.get(pk=kwargs['pk'])
        form = CourseForm(instance=course)
        return render(request, 'courses/manage/course/form.html', {'action':'update','form':form, 'pk':kwargs['pk']})
    
    def post(self, request, *args, **kwargs):
        instance = get_object_or_404(Course, pk=kwargs['pk'])
        form = CourseForm(request.POST, instance=instance)

        if form.is_valid():
            form.save()
            messages.success(request, "Course Updated Succesfully")            
            return render(request, 'courses/manage/course/form.html', {'action':'update','form':form, 'status':'updated','pk':kwargs['pk']})
        return (render(request, 'courses/manage/course/form.html', {'action':'update','status':'failed','pk':kwargs['pk']}))



class CourseDeleteView(PermissionRequiredMixin, View):
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'

    def get(self, request, *args, **kwargs):
        course = Course.objects.get(pk=kwargs['pk'])
        return render(request, self.template_name, {'action':'delete', 'object':course, 'pk':kwargs['pk']})

    def post(self, request, *args, **kwargs):
        instance = get_object_or_404(Course, pk=kwargs['pk'])
        if instance.delete():
            messages.success(request, "Course Deleted Succesfully")            
            return render(request, self.template_name, {'action':'delete','object':instance, 'status':'deleted','pk':kwargs['pk']})
        return (render(request, self.template_name, {'action':'delete','status':'failed','pk':kwargs['pk']}))

class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/formset.html'
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)
    
    def dispatch(self, request, pk):
        client_id = admin.get_client_id('website', request)
        logger.info(f'dispatch : CourseModuleUpdateView : {client_id} : {current_language} ')
        self.course = get_object_or_404(Course,
                                id=pk,
                                owner=request.user,
                                client_id=client_id,
                                language = current_language)
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
        client_id = admin.get_client_id('website', request)
        logger.info(f'dispatch : ContentCreatUpdateView : {client_id} : {current_language} ')
        self.module = get_object_or_404(Module, id=module_id, course__owner = request.user, client_id=client_id, language = current_language)
        self.model = self.get_model(model_name)
        if id:
            self.obj=get_object_or_404(self.model, id=id, owner=request.user, client_id=client_id, language = current_language)
        return super(ContentCreatUpdateView, self).dispatch(request, module_id, model_name, id)
    
    def get(self, request, module_id, model_name, id=None):
        form= self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form':form, 'object':self.obj})
    
    
    def post(self, request, module_id, model_name, id=None):
        client_id = admin.get_client_id('website', request)
        logger.info(f'POST : ContentCreatUpdateView : {client_id} : {current_language} ')
        form = self.get_form(self.model, 
                            instance=self.obj,
                            data=request.POST, 
                            files = request.FILES)
        if form.is_valid():
            
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                Content.objects.create(module=self.module, item=obj, client_id=client_id, language = current_language)
            return redirect('module_content_list', self.module.id)
        return self.render_to_response({'form':form, 'object':self.obj})

class ContentDeleteView(View):
    def post(self, request, id):
        client_id = admin.get_client_id('website', request)
        logger.info(f'POST : ContentDeleteView : {client_id} : {current_language} ')
        content = get_object_or_404(Content, id=id, module__course__owner = reqeust_user, client_id = client_id, language = current_language)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('module_content_list', module.id)

class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/content_list.html'

    def get(self, request, module_id):
        client_id = admin.get_client_id('website', request)
        logger.info(f'GET : ModuleContentListView : {client_id} : {current_language} ')
        module = get_object_or_404(Module, 
                                  id = module_id, 
                                  course__owner = request.user,
                                  client_id=client_id,
                                  language = current_language)
        return self.render_to_response({'module':module})


class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        client_id = admin.get_client_id('website', request)
        logger.info(f'POST : ModuleOrderView : {client_id} : {current_language} ')
        for id, order in self.request_json.items():
            Module.objects.filter(id = id, course__owner=request.user).filter(client_id=client_id).filter(language=current_language).update(order=order)
        return self.render_json_response({'saved':'OK'})
    

class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        client_id = admin.get_client_id('website', request)
        logger.info(f'POST : ContentOrderView : {client_id} : {current_language} ')
        for id , order in self.request_json.items():
            Content.objects.filter(id = id, module__course__owner=request.user).filter(language=current_language).filter(client_id=client_id).update(order=order)
        return self.render_json_reponse({'saved':'OK'})


class CourseListView(TemplateResponseMixin, View):
    model = Course
    template_name = 'home.html'

    def get(self, request, subject=None):
        
        client_id = admin.get_client_id('website', request)
        logger.info(f'GET : CourseListView : {client_id} : {current_language} ')
        subjects = Subject.objects.annotate(total_courses=Count('courses')).filter(language=current_language).filter(client_id = client_id)[:5]
        courses = Course.objects.annotate(total_modules = Count('modules')).filter(language=current_language).filter(client_id = client_id)[:12]
        instructors = Course.objects.values('owner__id').filter(language=current_language).filter(client_id = client_id).annotate(count=Count('owner_id')).values('client_id', 'owner__first_name','owner__last_name', 'owner__profiles__bio','owner__profiles__photo','count').order_by('-count')[:5]
        students_review = User.objects.filter(groups=4).values('first_name', 'last_name', 'profiles__photo')[:6]
    
        if subject:
            logger.info(f'GET : CourseListView : {subject} : {client_id} : {current_language} ')
            subject = get_object_or_404(Subject, slug=subject, client_id=client_id,language = current_language)
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
        client_id = admin.get_client_id('website', request)
        course = get_object_or_404(Course, slug=slug, client_id = client_id, language = current_language)
        instructor_ratings = InstructorRating.objects.filter(language=current_language).filter(client_id=client_id).annotate(avg_rating = Avg('rating')).annotate(review_count = Count('review')).annotate(students=Count('instructor__courses_created__students')).annotate(course_count = Count('instructor__courses_created', distinct=True)).filter(instructor = course.owner)
        course_avg_ratings = CourseRating.objects.all().filter(course=course.id).filter(language=current_language).filter(client_id=client_id).aggregate(Avg('rating'), Count('rating')) 
        total_ratings = course_avg_ratings['rating__count']
        course_ratings = CourseRating.objects.values(ratings = Round('rating')).filter(language=current_language).filter(course=course.id).filter(client_id=client_id).annotate(rating_count = Count('rating')*100/total_ratings).values('ratings','rating_count').order_by()
        
        add_to_cart_form = CartAddForm(initial={'course_id':course.id, 
                                                'price': course.price,
                                                'discount': 0,
                                                'coupon_code': None })
#       Create a rate counter for start ratng and % showing as that is not practical in template.
        course_wise_ratings = []
        ratings={}
        for i in range(5,0,-1):
            for course_rat in course_ratings:
                ratings = {}
                ratting = int(course_rat['ratings'])
                if i == ratting:
                     ratings['ratings'] = ratting
                     ratings['ratingspct'] = course_rat['rating_count']
                     break
                else:
                     ratings['ratings'] = i
                     ratings['ratingspct'] = '< 1'  
            if len(ratings) > 0:         
                course_wise_ratings.append(ratings)
        # test_i18n = _("testing")  
        # print(test_i18n)      
        return self.render_to_response({'course':course,
                                         'instructor_ratings':instructor_ratings,
                                         'course_avg_ratings':course_avg_ratings,
                                         'course_wise_ratings':course_wise_ratings,
                                         'add_to_cart_form':add_to_cart_form})


    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrolmentForm(initial={'course':self.object})
        return context
    

class SearchMain(TemplateResponseMixin, View):
    logger.info('SearchMain')
    template_name = "search_main.html"
    
    def get(self, request):
        client_id = admin.get_client_id('website', request)
        logger.info(f'get for {client_id}')
        search_term =request.GET.get('search_term')
        skill_filter = request.GET.get('hid_skill_filter')
        paid_filter  = request.GET.get('hid_paid_filter')
        hid_rating_filter =request.GET.get('hid_ratind_filter') 


        cart = Cart(request)
        print(cart.get_keys())

        if not search_term:
            search_term = ''

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
        # print(paid_filter
        courses = Course.objects.filter(Q(title__icontains=search_term)| Q(owner__first_name__icontains=search_term)).filter(language=current_language).filter(client_id=client_id).filter(level__in=qry_skill_filter).annotate(average_rating=Avg('course_review__rating')).values('id','title','slug', 'thumbnail_image','overview','duration','price','level','owner__first_name','owner__last_name').annotate(avg_rating=Avg('course_review__rating'))
        
        if (len(cart)) > 0:
            courses = courses.exclude(id__in = cart.get_keys())

        if hid_rating_filter:
            courses = courses.filter(avg_rating__gte = hid_rating_filter)
        # print(hid_skill_filter);
        return self.render_to_response({'result_courses':courses,
                                         'search_term':search_term,
                                         'hid_paid_filter':hid_paid_filter,
                                         'hid_skill_filter': hid_skill_filter,
                                         'hid_rating_filter' : hid_rating_filter})

class InstructorCourseView(View):
    def get(self, request, *args, **kwargs):
        # print(f'user - {request.user.groups__name}')
        courses = Course.objects.filter(owner=request.user)
        response = render(request, 'courses/course/course_list.html', {'courses': courses, 'view':'list_view'})
        return response