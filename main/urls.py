from main.apps import MainConfig
from django.urls import path
from main.views import LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, LessonUpdateAPIView, LessonDestroyAPIView, PaymentCreateAPIView, PaymentListAPIView
from rest_framework.routers import DefaultRouter
from main.views import CourseViewSet

app_name = MainConfig.name


router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

# urlpatterns = router.urls

urlpatterns = [

    #path('', HomeView.as_view(), name='homepage'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_delete'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_detail'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('payment/create/', PaymentCreateAPIView.as_view(), name='payment_create'),
    path('payment/', PaymentListAPIView.as_view(), name='payment_list'),


] + router.urls

