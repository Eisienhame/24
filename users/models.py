from django.db import models
from django.contrib.auth.models import AbstractUser


NULLABLE = {'blank': True, 'null': True}


class UserGroups(models.TextChoices):

    USERS = 'users', 'пользователи'
    MODERATORS = 'moderators', 'модераторы'


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='Номер телефона', **NULLABLE)
    country = models.CharField(max_length=100, verbose_name='Страна', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    role = models.CharField(max_length=10, choices=UserGroups.choices, default=UserGroups.USERS, verbose_name='роль', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

