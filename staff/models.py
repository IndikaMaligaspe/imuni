from django.db import models
from django.db.models import ForeignKey

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from home.models import Countries 
from courses.models import Course, Subject

User = get_user_model()
# Create your models here.

class Profiles(models.Model):

    email_display_choices=(  (0,_('Hide my email address from non-privilage users')),
                (1,_('Allow everyone to see my email address')),
                (2,_('Allow only course members to see my email address')),
            )
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    bio=models.TextField(_('bio'))
    photo=models.ImageField(upload_to='users/%Y/%m/%d/',blank=True)
    city=models.CharField(_('city'),max_length=50, db_index=True, default=None)
    country=models.ForeignKey(Countries, related_name='profile_country', on_delete=models.CASCADE)
    email_display=models.CharField(_('email_display'), max_length=500, 
                             choices = email_display_choices, 
                             default=0)
    webpage=models.CharField(_('webpage'),max_length=50, db_index=True, default=None)
    phone=models.CharField(_('phone'),max_length=50, db_index=True, default=None)
    mobile=models.CharField(_('mobile'),max_length=50, db_index=True, default=None)
    address=models.CharField(_('address'),max_length=500, db_index=True, default=None)
    language=models.CharField(max_length=20, db_index=True, default='en')
    client_id= models.IntegerField(db_index=True, default=0)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

    # def get_absolute_url(self):
    #     return reverse('images:detail',args=[self.id, self.slug])
