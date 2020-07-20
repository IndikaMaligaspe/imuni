from django.urls import path 
from django.conf.urls.i18n import i18n_patterns
from . import views 

urlpatterns = [
    path('create/', views.InstructorCreateAccount.as_view(), name='instructor_create'),
]