from django.shortcuts import render, redirect
from django.views.generic.base import TemplateResponseMixin, View
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .cart import Cart
from .forms import CartAddForm
from courses.models import  Course

# Create your views here.

user = get_user_model()


class AddToCart(TemplateResponseMixin, View):
    model = Cart 
    template_name = 'cart/add_to_cart.html'
    
    
    def post(self, request, *args, **kwargs):
        cart = {}
        course = None
        form = CartAddForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            course_id = cd['course_id']
            cart = Cart(request)
            course = Course.objects.filter(id = course_id).get()
            # cart.clear()
            cart.add(course)
            cart.save()
            for item in cart:
                print(item)
        return self.render_to_response({'cart':cart, 'course':course})

    def get(self, request):
        remove_id = request.GET.get('remove_id')
        clear = request.GET.get('clear')
            
        print (remove_id)
        cart = Cart(request)
        if(clear):
            cart.clear()
            return redirect('search_main')

        if remove_id:
            cart.remove(remove_id)
            cart.save()
            if len(cart) == 0:
                return redirect('search_main')
        return self.render_to_response({'cart':cart})
