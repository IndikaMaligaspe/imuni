from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Countries(models.Model):
    country_code = models.CharField(max_length=10)
    country_name = models.CharField(_('country'), max_length=200)

    def __str__(self):
        return 'Country {}'.format(self.country_name)
