from django.db import models

# To Create A Custom User Model and admin panel
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy



# Create your models here.


class MyuserManager(
    BaseUserManager
):  # To Manage new users using this baseusermanaegr class
    """ A Custom User Manager to deal with Emails  as an unique Identifier """

    def _create_user(self, email, username, password, **extra_fields):
        """Creates and Saves an user with given email and password """

        if not email:
            raise ValueError("Email Must Be Set")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("SuperUser is_staff must be True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("SuperUser is_superuser must be True")

        return self._create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False)
    username = models.CharField(max_length=264,unique=True)
    is_teacher=models.BooleanField(default=True)
    is_student=models.BooleanField(default=False)
    is_staff = models.BooleanField(
        gettext_lazy("staff_status"),
        default=False,
        help_text="Determines Whether They Can Log in this Site or not",
    )
    is_active = models.BooleanField(
        gettext_lazy("active"),
        default=True,
        help_text="Determines Whether their Account Status is Active or not",
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    objects = MyuserManager()

    class Meta:
        verbose_name_plural = "User"
        db_table = "User"

    def __str__(self):
        return self.username

def upload_image(instance, filename):
    return "profile/{instance.user.username}--{filename}".format(instance=instance,filename=filename)


class Profile(models.Model):
    full_name = models.CharField(max_length=264, blank=True)
    profile_pic=models.ImageField(upload_to=upload_image,blank=True,default='/profile/avatar.jpg')    
    phone = models.CharField(max_length=20, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def is_fully_filled(self):
        fields_name = [f.name for f in self._meta.get_fields()]

        for fields in fields_name:
            value = getattr(self, fields)
            if value is None or value == "":
                return False
        return True


class Teacher(Profile):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="teacher")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Teacher"




class Student(Profile):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name_plural = "Student"
