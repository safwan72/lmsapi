from django.urls import path,re_path
from . import views
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r"newteacher", views.TeacherCreateSerializerView, basename='newteacher'),
router.register(r"newstudent", views.StudentCreateSerializerView, basename='newstudent')

urlpatterns = [
    path('studentupdate/<user>/',views.StudentProfileUpdateView.as_view(),name='studentupdate'),
    path('teacherupdate/<user>/',views.TeacherProfileUpdateView.as_view(),name='teacherupdate'),
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    ]+router.urls
