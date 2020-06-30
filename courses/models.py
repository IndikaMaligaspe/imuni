from django.db import models
from django.db.models import ForeignKey

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
 

User = get_user_model()

class Subject(models.Model):
    title= models.CharField(_('title'), max_length=200)
    slug= models.SlugField(max_length=200, unique=True)
    language = models.CharField(max_length=20, db_index=True, default='en')
    client_id= models.IntegerField(db_index=True, default=0)
      

    class Meta:
        ordering  = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Subject_detail", kwargs={"pk": self.pk})


class Course(models.Model):

    BEGINNER = 'Beginner'
    INTERMEDIATE = 'Intermediate'
    ADVANCED = 'Advanced'
    ALL_LEVELS ='All Levels'

    level_choices = (  (BEGINNER , 'Beginner'),
                (INTERMEDIATE,'Intermediate'),
                (ADVANCED,'Advanced'),
                (ALL_LEVELS,'All Levels'),
            )


    owner = models.ForeignKey(User,  related_name='courses_created', on_delete=models.CASCADE)    
    subject = models.ForeignKey(Subject, related_name='courses', on_delete=models.CASCADE)
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField(_('overview'))
    requirements = models.TextField(_('overview'),blank=True)
    content_summary = models.TextField(_('content_summary'),blank=True) 
    created = models.DateTimeField(_('created'), auto_now=False, auto_now_add=True)  
    students = models.ManyToManyField(User,
                                 related_name='courses_joined',
                                 blank=True)
    thumbnail_image = models.ImageField(upload_to='courses/%Y/%m/%d/',blank=True)
    duration = models.FloatField(default=5)
    level = models.CharField(_('level'), max_length=50, 
                             choices = level_choices, 
                             default=ALL_LEVELS)
    price  = models.FloatField(default=21)
    language = models.CharField(max_length=20, db_index=True, default='en')
    client_id= models.IntegerField(db_index=True, default=0)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Course_detail", kwargs={"pk": self.pk})
    
    def get_instructors(self):
        return '{} {}'.format(self.owner.first_name, self.owner.last_name)

class Module(models.Model):
    course = models.ForeignKey(Course,  related_name='modules', on_delete=models.CASCADE)     
    title = models.CharField(_('title'), max_length=200)
    description = models.TextField(_('description'),blank=True)
    order = OrderField(blank=True, for_fields=['course'])
    language = models.CharField(max_length=20, db_index=True, default='en')
    client_id= models.IntegerField(db_index=True, default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '{}. {}'.format(self.order, self.title)

    def get_absolute_url(self):
        return reverse("Module_detail", kwargs={"pk": self.pk})

class Content(models.Model):
    module = models.ForeignKey(Module, related_name='content', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, 
                                     limit_choices_to={'model__in':('text', 'video','image','file')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type','object_id')
    order = OrderField(blank=True, for_fields=['module'])
    language = models.CharField(max_length=20, db_index=True, default='en')
    client_id= models.IntegerField(db_index=True, default=0)

    class Meta:
        ordering = ['order']

class ItemBase(models.Model):
    owner = models.ForeignKey(User, related_name='%(class)s_related', on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    language = models.CharField(max_length=20, db_index=True, default='en')
    client_id= models.IntegerField(db_index=True, default=0)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title
    
    def render(self):
        return render_to_string('courses/content/{}.html'.format(
                                self._meta.model_name),{'item':self})

class Text(ItemBase):
    content = models.TextField()
    language = models.CharField(max_length=20, db_index=True, default='en')
    client_id= models.IntegerField(db_index=True, default=0)

class File(ItemBase):
    file = models.FileField(upload_to='files')
    language = models.CharField(max_length=20, db_index=True, default='en')
    client_id= models.IntegerField(db_index=True, default=0)

class Image(ItemBase):
    file = models.FileField(upload_to='images')
    language = models.CharField(max_length=20, db_index=True, default='en')
    client_id= models.IntegerField(db_index=True, default=0)

class video(ItemBase):
    url = models.URLField()
    language = models.CharField(max_length=20, db_index=True, default='en')
    client_id= models.IntegerField(db_index=True, default=0)

class Profiles(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(_('bio'))
    photo = models.ImageField(upload_to='users/%Y/%m/%d/',blank=True)
    language = models.CharField(max_length=20, db_index=True, default='en')
    client_id= models.IntegerField(db_index=True, default=0)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

    # def get_absolute_url(self):
    #     return reverse('images:detail',args=[self.id, self.slug])

class CourseRating(models.Model):
    
    rate_choices = ( (1,1),
                     (1.5,1.5),
                     (2,2),
                     (2.5,2.5),
                     (3, 3),
                     (3.5,3.5),
                     (4,4),
                     (4.5,4.5),
                     (5,5))

    user = models.ForeignKey(User, related_name='student_review', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='course_review', on_delete=models.CASCADE)
    review = models.TextField(_('review'))
    review_date = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0,choices=rate_choices)
    language = models.CharField(max_length=20, db_index=True, default='en')
    client_id= models.IntegerField(db_index=True, default=0)

    def __str__(self):
        return '{} on {}'.format(self.user.username, self.course.title)

class InstructorRating(models.Model):
    rate_choices = ( (1,1),
                     (1.5,1.5),
                     (2,2),
                     (2.5,2.5),
                     (3, 3),
                     (3.5,3.5),
                     (4,4),
                     (4.5,4.5),
                     (5,5))

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    instructor = models.ForeignKey(User, related_name='instructor_review', on_delete=models.CASCADE)
    review = models.TextField(_('review'))
    review_date = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0,choices=rate_choices)
    language = models.CharField(max_length=20, db_index=True, default='en')
    client_id= models.IntegerField(db_index=True, default=0)

    def __str__(self):
        return '{} on {}'.format(self.student.username, self.instructor.username)

class SiteReview(models.Model):
    student = models.ForeignKey(User, related_name='site_review', on_delete=models.CASCADE)
    review = models.TextField(_('review'))
    review_date = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=20, db_index=True, default='en')
    client_id= models.IntegerField(db_index=True, default=0)