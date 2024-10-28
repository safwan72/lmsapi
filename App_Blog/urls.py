from django.urls import path
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r"blog", views.BlogSerializerView, basename='blog'),
router.register(r"comment", views.CommentSerializerView, basename='comment'),
# router.register(r"answer_quiz", views.AnswerView, basename='answer_quiz'),
# router.register(r"graded_quiz", views.GradedQuizView, basename='graded_quiz'),

urlpatterns = [
    path('blog_detail/<slug>/',views.BlogDetailSerializerView.as_view(),name='blog_detail'),
    path('blog_create/',views.BlogCreateSerializerView.as_view(),name='blog_create')
    ]+router.urls
