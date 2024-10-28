from django.urls import path
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r"question", views.QuestionSerializerView, basename='question'),
router.register(r"quiz", views.QuizSerializerView, basename='quiz'),
router.register(r"stu_quiz", views.StudentAllQuizSerializerView, basename='stu_quiz'),
router.register(r"answer_quiz", views.AnswerView, basename='answer_quiz'),
router.register(r"graded_quiz", views.GradedQuizView, basename='graded_quiz'),

urlpatterns = [
path('individualquiz/<int:id>/',views.QuizIndividualView.as_view(),name='individualquiz'),
path('studentques/<pk>/',views.StudentQuestionSerializerView.as_view(),name='studentques')
]+router.urls
