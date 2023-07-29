from django.shortcuts import render
from main.models import Lesson, Course, SubscriptionCourse
from django.urls import reverse_lazy, reverse
from rest_framework import viewsets, generics
from main.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionCourseSerializers
from main.models import Course, Lesson, Payment
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from main.permissions import ModeratorsPermissions, UsersPermissions
from main.services import StripeApi
from users.models import UserGroups
from main.paginators import LessonPaginator
from rest_framework.response import Response


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated | ModeratorsPermissions | UsersPermissions]
    pagination_class = LessonPaginator

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
    pagination_class = LessonPaginator

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
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated | ModeratorsPermissions | UsersPermissions]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated | ModeratorsPermissions | UsersPermissions]


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        user = self.request.user

        user_data = serializer.validated_data

        intent = StripeApi()
        stripe_data = intent.create_payment_intent(user_data=user_data, user=user)  # вызов метода по созданию платежа
        serializer.save(user=user, status=stripe_data[1],
                        stripe_id=stripe_data[0])  # сохранение в модели данных полученных от stripe


class PaymentConfirm(generics.RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        intent = StripeApi()

        instance.status = intent.confirm_intent(
            instance.stripe_id)  # вызов метода по подтверждению платежа и обновление статуса платежа в бд
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)



class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['payed_lesson', 'payed_course', 'how_payed']
    ordering_fields = ['payment_date']


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionCourseSerializers
    queryset = SubscriptionCourse.objects.all()
    permission_classes = [IsAuthenticated]


class SubscriptionUpdateView(generics.UpdateAPIView):
    serializer_class = SubscriptionCourseSerializers
    queryset = SubscriptionCourse.objects.all()
    permission_classes = [IsAuthenticated]

