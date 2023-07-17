from main.apps import MainConfig
from django.urls import path
from main.views import LessonCreateView, LessonDeleteView, LessonDetailView, LessonUpdateView, LessonListView
from rest_framework.routers import DefaultRouter
from main.views import CourseViewSet

app_name = MainConfig.name


router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [

    #path('', HomeView.as_view(), name='homepage'),
    path('lesson_list/', LessonListView.as_view(), name='lesson_list'),
    path('lesson_list/create/', LessonCreateView.as_view(), name='lesson_create'),
    path('lesson_list/delete/<int:pk>/', LessonDeleteView.as_view(), name='lesson_delete'),
    path('lesson_list/<int:pk>/', LessonDetailView.as_view(), name='lesson_detail'),
    path('lesson_list/update/<int:pk>/', LessonUpdateView.as_view(), name='lesson_update'),


] + router.urls

