from django.db import models

# Create your models here.

class Cart(models.Model):
    
    def __str__(self):
        pass

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'