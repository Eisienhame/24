from rest_framework import serializers
from main.models import Course, Lesson, Payment, SubscriptionCourse
from main.validators import UrlValidator


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [UrlValidator(field='url')]


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True, source='lesson_set')
    number_of_lesson = serializers.SerializerMethodField()
    subscribers = serializers.SerializerMethodField()

    def get_number_of_lesson(self, course):

        lesson = Lesson.objects.filter(course=course)
        if lesson:
            return lesson.count()
        return 0

    def get_subscribers(self, instance):
        user = self.context['request'].user

        if SubscriptionCourse.objects.filter(user=user, course=instance).exists():
            return True
        else:
            return False

    class Meta:
        model = Course
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'


class SubscriptionCourseSerializers(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionCourse
        fields = "__all__"

