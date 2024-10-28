from rest_framework import serializers
from . import models
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ("username", "email", "password",'is_teacher','is_student')
        extra_kwargs = {
            "password": {"write_only": True, "style": {"input_type": "password"}}
        }

    def create(self, validated_data):
        user = models.User.objects._create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user


class TeacherProfileSerialzer(serializers.ModelSerializer):
    user=UserSerializer(required=True)
    
    class Meta:
        model = models.Teacher
        fields = ("user",)

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_data['is_teacher']=True
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        user.is_teacher=True
        user.is_student=False
        user.save()
        teacher, created = models.Teacher.objects.update_or_create(
            user=user, **validated_data
        )
        return teacher


class StudentProfileSerialzer(serializers.ModelSerializer):
    user=UserSerializer(required=True)
    
    class Meta:
        model = models.Student
        fields = ("user",)

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_data['is_student']=True
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        user.is_teacher=False
        user.is_student=True
        user.save()
        student, created = models.Student.objects.update_or_create(
            user=user, **validated_data
        )
        return student
    
    

class StudentProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = "__all__"

class TeacherProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Teacher
        fields = "__all__"
        
        
        
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['is_student'] = user.is_student
        token['is_teacher'] = user.is_teacher
        return token