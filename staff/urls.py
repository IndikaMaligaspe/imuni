from django.urls import path 
from django.conf.urls.i18n import i18n_patterns
from . import views 

urlpatterns = [
    path('create/', views.InstructorCreateOrUpdateAccount.as_view(), name='instructor_create'),
    path('create/<int:staff_id>', views.InstructorCreateOrUpdateAccount.as_view(), \
        name='instructor_update'),

]