from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id','email','first_name','last_name','phone_number','national_id']


class UserProfileSerializer(serializers.ModelSerializer):
	jobs_applied = serializers.StringRelatedField(many=True)
	class Meta:
		model = User
		exclude = ['password', 'is_superuser','groups','user_permissions','last_login']
