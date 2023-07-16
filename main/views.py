from django.shortcuts import render
from django.views import generic
from main.models import Lesson
from django.urls import reverse_lazy, reverse


class LessonListView(generic.ListView):
    model = Lesson


class LessonDetailView(generic.DetailView):
    model = Lesson


class LessonCreateView(generic.CreateView):
    model = Lesson
    success_url = reverse_lazy('main:lesson_list')
    fields = ('name', 'description', 'preview', 'url')


class LessonDeleteView(generic.DeleteView):
    model = Lesson
    success_url = reverse_lazy('main:lesson_list')


class LessonUpdateView(generic.UpdateView):
    model = Lesson
    success_url = reverse_lazy('main:lesson_list')
    fields = ('name', 'description', 'preview', 'url')