from decimal import Decimal
from django.conf import settings
from courses.models import Course

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    
    def add(self, course):
        course_id = str(course.id)
        
        if course_id not in self.cart:
            self.cart[course_id] = {'id':course_id, 'title':course.title, 'instructor':course.get_instructors(),'price':str(course.price),'thumbnail':course.thumbnail_image.path, 'subject_id':course.subject_id}
        self.save()
    
    def save(self):
        self.session.modified = True
    
    def remove(self, course_id):
        if course_id in self.cart:
            del self.cart[course_id]
    
    def __iter__(self):
        cart = self.cart.copy()
        for item in cart.values():
            yield item
    
    def __len__(self):
        return len(self.cart)

    def get_total_price(self):
        return sum(Decimal(item['price']) for item in self.cart.values())
    
    def get_item_count(self):
        return len(self.cart)
    
    def get_keys(self):
        if len(self.cart) > 0:
            return list(self.cart.keys())

    def get_subject_list(self):
       subject_list = []
       for item in self.cart.values():
           subject_list.append(item['subject_id'])
       return subject_list

    def get_course_list(self):
       course_list = []
       for item in self.cart.values():
           course_list.append(item['id'])
       return course_list

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()


