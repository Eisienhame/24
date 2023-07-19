from rest_framework import serializers
from main.models import Course, Lesson, Payment


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True, source='lesson_set')
    number_of_lesson = serializers.SerializerMethodField()

    def get_number_of_lesson(self, course):

        lesson = Lesson.objects.filter(course=course)
        if lesson:
            return lesson.count()
        return 0



    class Meta:
        model = Course
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'

