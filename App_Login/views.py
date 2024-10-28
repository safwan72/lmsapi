from django.shortcuts import render
from . import models,serializers,permissions
from rest_framework import viewsets,generics,mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
class TeacherCreateSerializerView(viewsets.ModelViewSet):
    queryset=models.Teacher.objects.all()
    serializer_class=serializers.TeacherProfileSerialzer

class StudentCreateSerializerView(viewsets.ModelViewSet):
    queryset=models.Student.objects.all()
    serializer_class=serializers.StudentProfileSerialzer
    lookup_field='user__username'

class StudentProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset=models.Student.objects.all()
    serializer_class=serializers.StudentProfileUpdateSerializer
    lookup_field='user'
    # permission_classes=[permissions.IsStudentPermisson]


class TeacherProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset=models.Teacher.objects.all()
    serializer_class=serializers.TeacherProfileUpdateSerializer
    lookup_field='user'
    
    
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.MyTokenObtainPairSerializer