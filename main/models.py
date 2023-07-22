from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    preview = models.ImageField(upload_to='main/', verbose_name='изображение', **NULLABLE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель', **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'
        ordering = ('name',)


class Lesson(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    preview = models.ImageField(upload_to='main/', verbose_name='изображение', **NULLABLE)
    url = models.URLField(verbose_name='ссылка на видео')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', **NULLABLE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель', **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
        ordering = ('name',)


class Payment(models.Model):
    CHOICES_PAY = [
        ('Card', 'Карта'),
        ('Cash', 'Наличные')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    payment_date = models.DateField(auto_now_add=True, verbose_name='Дата оплаты')
    payed_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Оплаченный курс', **NULLABLE)
    payed_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Оплаченный урок', **NULLABLE)
    sum_payed = models.IntegerField(verbose_name='Сумма оплаты')
    how_payed = models.CharField(choices=CHOICES_PAY, verbose_name='Способ оплаты')


    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name = 'оплата'
        verbose_name_plural = 'платежи'
        ordering = ('payment_date',)


class SubscriptionCourse(models.Model):
    status = models.BooleanField(default=True, verbose_name='Статус подписки')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')

    class Meta:
        verbose_name = "подписка"
        verbose_name_plural = "подписки"


