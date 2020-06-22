from django.shortcuts import render, get_object_or_404, redirect, render, reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from datetime import datetime
from django.http import HttpResponse

from cart.cart import Cart 
from courses.models import Course
from .models import Order , OrderItem
# Create your views here.

# User = get_user_model()
def order_create(request):
    cart = Cart(request)

    if request.method == 'POST':
        order_type = request.POST['order_type']
        if 'student_enrol_course' in order_type:

            order = Order(order_by=request.user, created=datetime.now(), paid=False)
            # if cart.coupon:
            order.save()
            for item in cart:
                course = get_object_or_404(Course,id=item['id'])
                OrderItem.objects.create(order = order,
                                        course = course,
                                        price = item['price'],
                                        quantity=1)

            request.session['order_id'] = order.id 
            # return redirect(reverse('payment:process'))    
            return render(request,'orders/order/order_confirm.html',{'order':order})                       
    else:
        return HttpResponse('Method not implemented...')
