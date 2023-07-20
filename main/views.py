from django.shortcuts import render
from main.models import Lesson, Course
from django.urls import reverse_lazy, reverse
from rest_framework import viewsets, generics
from main.serializers import CourseSerializer, LessonSerializer, PaymentSerializer
from main.models import Course, Lesson, Payment
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from main.permissions import ModeratorsPermissions, UsersPermissions
from users.models import UserGroups


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated | ModeratorsPermissions | UsersPermissions]

    # def get_queryset(self):
    #     user = self.request.user
    #     if user.is_staff or user.is_superuser or (user.role == UserGroups.MODERATORS):
    #         return Lesson.objects.all()
    #     else:
    #         return Lesson.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser or (user.role == UserGroups.MODERATORS):
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated | ModeratorsPermissions | UsersPermissions]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated | ModeratorsPermissions | UsersPermissions]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated | ModeratorsPermissions | UsersPermissions]


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['payed_lesson', 'payed_course', 'how_payed']
    ordering_fields = ['payment_date']
