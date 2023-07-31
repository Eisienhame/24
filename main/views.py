from django.shortcuts import render
from main.models import Lesson, Course, SubscriptionCourse
from django.urls import reverse_lazy, reverse
from rest_framework import viewsets, generics, status
from main.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionCourseSerializers
from main.models import Course, Lesson, Payment
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from main.permissions import ModeratorsPermissions, UsersPermissions
from main.services import create_payment, checkout_session
from main.tasks import send_updated_email
from users.models import UserGroups
from main.paginators import LessonPaginator
from rest_framework.response import Response
from rest_framework.views import APIView
import stripe


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated | ModeratorsPermissions | UsersPermissions]
    pagination_class = LessonPaginator

    def update(self, request, *args, **kwargs):
        send_updated_email(kwargs['pk'])

        return super().update(request, *args, **kwargs)

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

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session = checkout_session(
            course=serializer.validated_data['payed_course'],
            user=self.request.user
        )
        serializer.save()
        create_payment(course=serializer.validated_data['payed_course'],
                       user=self.request.user)
        return Response(session['id'], status=status.HTTP_201_CREATED)


class GetPaymentView(APIView):
    """Получение информации о платеже"""
    def get(self, request, payment_id):
        payment_intent = stripe.PaymentIntent.retrieve(payment_id)
        return Response({
            'status': payment_intent.status, })


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

