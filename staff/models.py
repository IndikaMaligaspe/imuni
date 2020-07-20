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
    city=models.CharField(_('city'),max_length=50, db_index=True, default='en')
    country=models.CharField(_('country'),max_length=50, db_index=True, default='en')
    email_display=models.CharField(_('email_display'), max_length=500, 
                             choices = email_display_choices, 
                             default=0)
    webpage=models.CharField(_('webpage'),max_length=50, db_index=True, default='en')
    phone=models.CharField(_('phone'),max_length=50, db_index=True, default='en')
    mobile=models.CharField(_('mobile'),max_length=50, db_index=True, default='en')
    address=models.CharField(_('address'),max_length=500, db_index=True, default='en')
    language=models.CharField(max_length=20, db_index=True, default='en')
    client_id= models.IntegerField(db_index=True, default=0)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

    # def get_absolute_url(self):
    #     return reverse('images:detail',args=[self.id, self.slug])
