from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from courses.models import Course


# Create your models here.

class Order(models.Model):
    order_by = models.ForeignKey(User,related_name='ordered_by', null=False, blank=False, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateField(auto_now=True, auto_now_add=False)
    paid = models.BooleanField(default=False)
    pan_id = models.CharField(max_length=150, blank=True)
    language = models.CharField(max_length=20, db_index=True, default='en')
    client_id= models.IntegerField(max_length=20, db_index=True, default=0)# coupon = models.ForeignKey(Coupon, related_name='orders', null=True, blank=True, on_delete=models.CASCADE)
    # discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
 
    def __str__(self):
        return f'{self.created}:{self.updated}:{self.braintree_id}:{self.paid}'
    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost 
        # - total_cost* (self.discount/ Decimal('100'))

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name = 'order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    language = models.CharField(max_length=20, db_index=True, default='en')
    client_id= models.IntegerField(max_length=20, db_index=True, default=0)

    def __str__(self):
        return '{}'.format(self.id)
    
    def get_cost(self):
        return self.price * self.quantity
