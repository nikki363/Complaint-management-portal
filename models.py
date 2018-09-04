from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
'''class User(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,default='')
    mobilenumber=models.IntegerField()
    department=models.CharField(max_length=20,default='')
    emailid=models.EmailField(default='')
    address=models.CharField(max_length=100,default='')
    employeeid=models.IntegerField()'''


from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        #email = self.normalize_email(email)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self,username,  password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    #user = models.OneToOneField(User, on_delete=models.CASCADE, default='')
    mobilenumber = models.IntegerField()
    department = models.CharField(max_length=20, default='')
    address = models.CharField(max_length=100, default='')
    employeeid = models.IntegerField(default=1)
    email= models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('username'), max_length=30,unique=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_admin = models.BooleanField(_('active'), default=False)
    is_superuser = models.BooleanField(_('active'), default=False)
    is_staff = models.BooleanField(_('staff'), default=False)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

class Complaints(models.Model):
    complaint_id=models.AutoField(primary_key=True)
    created_DateTime=models.DateTimeField(auto_now_add=True)
    complaint_title=models.CharField(max_length=200)
    complaint_department=models.CharField(max_length=50)
    complaint_description=models.TextField()
    complaint_priority=models.CharField(max_length=10,default='')
    complaint_status=models.CharField(max_length=20)
    complaint_username=models.CharField(max_length=20)
    complaint_email=models.EmailField()




class DepartmentDetails(models.Model):
    department_id=models.IntegerField(default=1)
    department_name=models.CharField(max_length=20)
    department_grpemail=models.EmailField()
'''
class Permission(User):
    class Meta:
        proxy=True
        permissions=(
            ('Admin','Administration'),
            ('Networks ','Network '),
            ('Human resources ','Human resources '),
            ('Engineers','Engineers')

        )'''
class DepartmentAdmins_list(models.Model):
    d_id=models.IntegerField(default=1)
    d_name=models.CharField(max_length=30,default='')
    d_username=models.CharField(max_length=40,default='')

class ComplaintAssignment(models.Model):
    comp_id=models.IntegerField(default='')
    dep_name = models.CharField(max_length=50,default='')
    complaint_assignment=models.CharField(max_length=30, default='')
class Comments(models.Model):
    complaint_name=models.CharField(max_length=50,default='')
    response_no=models.AutoField(primary_key=True ,default=1)
    comment=models.TextField(default='')