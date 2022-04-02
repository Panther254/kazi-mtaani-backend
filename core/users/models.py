from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created


# Create your models here.
class UserAccountManager(BaseUserManager):
	
	def create_user(self, email, password=None,**extra_fields):
		if not email:
			raise ValueError("User must have an email address")
		email = self.normalize_email(email)
		user = self.model(email=email,**extra_fields)
		user.set_password(password)
		user.save()

		return user

	def create_superuser(self, email,password=None,**extra_fields):
		user = self.create_user(email,password)

		user.is_superuser = True
		user.is_staff = True
		user.save()

		return user
		
class UserAccount(AbstractBaseUser, PermissionsMixin):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.EmailField(max_length=255,unique=True)
	phone_number = models.CharField(unique=True,max_length=20,null=True)
	residence = models.CharField(max_length=255,null=True)
	national_id = models.CharField(unique=True,max_length=255,null=True)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = UserAccountManager()

	def get_full_name(self):
		return f"{self.first_name} {self.last_name}"

	def get_short_name(self):
		return self.first_name

	def __str__(self):
		return self.email