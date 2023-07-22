from rest_framework.test import APITestCase
from rest_framework import status

from main.models import Lesson, Course, SubscriptionCourse
from users.models import User


class CourseTestCase(APITestCase):

    def setUp(self) -> None:
        super().setUp()
        self.lesson = Lesson.objects.create(
            id='5',
            name='Тест1',
            description='Тест',
            url='https://www.youtube.com/watch?v=5vVwjSIixuQ'

        )
        self.user = User.objects.create(
            email='test@yandex.ru',
            is_superuser=True

        )
        self.user.set_password('12345678')
        self.user.save()
        response = self.client.post(
            '/users/token/',
            {
                'email': 'test@yandex.ru',
                'password': '12345678'
            }
        )

        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_create_lesson(self):
        response = self.client.post(
            '/lesson/create/',
            {'name': 'Тест2',
             'description': 'Тест',
             'url':'https://www.youtube.com/watch?v=5vVwjSIixuQ'}
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_get_all_lessons(self):
        response = self.client.get(
            '/lesson/'

        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_delete_lesson(self):
        response = self.client.delete(
            '/lesson/delete/5/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_lesson_retrieve(self):
        response = self.client.get(
            '/lesson/5/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )


class SubscriptionTest(APITestCase):
    def setUp(self) -> None:
        super().setUp()
        self.course = Course.objects.create(
            name='Test',
            description='Test'
        )
        self.user = User.objects.create(
            id='1',
            email='test@yandex.ru',
            is_superuser=True
        )
        self.user.set_password('12345678')
        self.user.save()
        response = self.client.post(
            '/users/token/',
            {
                'email': 'test@yandex.ru',
                'password': '12345678'
            }
        )

        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_create_subscription(self):
        response = self.client.post(
            '/subscription/create/',
            {
                "status": "True",
                "user": "1",
                "course": "1"
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )