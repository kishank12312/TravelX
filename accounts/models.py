from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name = 'email', max_length = 250, unique = True)
    username = models.CharField(max_length = 100, unique = True)
    date_of_birth = models.DateField(verbose_name = 'Date of birth')
    date_joined	= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)