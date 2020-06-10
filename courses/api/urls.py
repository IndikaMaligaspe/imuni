from django.urls import path , include
from courses.api import views
from rest_framework import routers

app_name = 'courses'

router = routers.DefaultRouter()
router.register('courses', views.CourseViewSet)
urlpatterns = [
    path('subjects/', views.SubjectListView.as_view(), name='subject_list'),
    path('subject/<pk>/', views.SubjectDetailView.as_view(), name='subject_detail'),
    path('', include(router.urls)),
]