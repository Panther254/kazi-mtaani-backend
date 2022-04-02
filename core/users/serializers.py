from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id','email','first_name','last_name','phone_number','national_id']


class UserProfileSerializer(serializers.ModelSerializer):
	jobs_applied = serializers.StringRelatedField(many=True)
	class Meta:
		model = User
		exclude = ['password', 'is_superuser','groups','user_permissions','last_login']

class ChangePasswordSerializer(serializers.Serializer):
	model = User
	old_password = serializers.CharField(required=True)
	new_password = serializers.CharField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
	email = serializers.EmailField(min_length=5)

	class Meta:
		fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
	password = serializers.CharField(min_length=6,write_only=True)
	token = serializers.CharField(min_length=1,write_only=True)
	uidb64 = serializers.CharField(min_length=1,write_only=True)

	class Meta:
		fields = ['password','token','uidb64']

	def validate(self,attrs):
		try:
			password = attrs.get('password')
			token = attrs.get('token')
			uidb64 = attrs.get('uidb64')

			user_id = force_str(urlsafe_base64_decode(uidb64))
			user = User.objects.get(id=user_id)


			if not PasswordResetTokenGenerator().check_token(user,token):
				raise AuthenticationFailed("The reset link in invalid",401)

			user.set_password(password)
			user.save()
			return user
		except DjangoUnicodeDecodeError as identifier:
			raise AuthenticationFailed("The reset link in invalid",401)

		return super().validate(attrs)