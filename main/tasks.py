from celery import shared_task
from django.core.mail import send_mail

from config import settings
from main.models import SubscriptionCourse


@shared_task
def send_updated_email(course):
    subscribers = SubscriptionCourse.objects.get(course=course)
    send_mail(
        'ALARM!',
        f'Сообщаем, что курс на который вы подписаны  обновлён',
        settings.EMAIL_HOST_USER,
        [subscribers.user]
    )