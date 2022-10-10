from .utils import Util
from .serializers import (ChangePasswordSerializer, ResetPasswordSerializer,
                          SetNewPasswordSerializer, UserProfileSerializer,
                          UserSerializer)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import (
    DjangoUnicodeDecodeError, smart_bytes, smart_str)
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

User = get_user_model()


# Create your views here.
@method_decorator(csrf_protect, name='dispatch')
class CheckAuthenticated(APIView):
    def get(self, request, format=None):
        is_authenticated = User.is_authenticated
        if is_authenticated:
            return Response({'is_authenticated': True })
        else:
            return Response({'is_authenticated': False })


@method_decorator(csrf_protect, name='dispatch')
class SignUpView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        data = self.request.data

        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        phone_number = data['phone_number']
        national_id = data['national_id']
        password = data['password']
        re_password = data['re_password']

        try:
            if password == re_password:
                if User.objects.filter(email=email).exists():
                    return Response({'error': 'Email is already registered.'})
                if User.objects.filter(national_id=national_id).exists():
                    return Response({'error': 'The National ID is already registred'})

                user = User.objects.create_user(email=email, password=password, first_name=first_name,
                                                last_name=last_name, phone_number=phone_number, national_id=national_id)
                user.save()
                content = {"success": "User created sucessfully."}
                return Response(content, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Passwords do not match.'})
        except:
            return Response({'error': 'Something went wrong'})


@method_decorator(csrf_protect, name='dispatch')
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        data = self.request.data

        email = data['email']
        password = data['password']

        try:
            user = auth.authenticate(email=email, password=password)
            if user is not None:
                auth.login(request, user)
                return Response({'success': 'Login sucessful'}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'error': 'Invalid email/password'}, status=status.HTTP_202_ACCEPTED)
        except:
            return Response({'error': 'Something went wrong'},status=status.HTTP_406_NOT_ACCEPTABLE)


class LogoutView(APIView):
    def post(self, request, format=None):
        try:
            auth.logout(request)
            return Response({'success': 'Logging out sucessful'})
        except:
            return Response({'error': 'Something went wrong when logging out'})


@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        return Response({"success": "Token cookie has been sucessfully set"})


class DeleteAccountView(APIView):
    def delete(self, request, format=None):
        user = self.request.user
        try:
            user = User.objects.filter(id=user.id).delete()
            return Response({'success': 'User deleted sucessfully'})
        except:
            return Response({'error': 'Something went wrong trying to delete user'})


class GetUsersView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        users = User.objects.all()

        users = UserSerializer(users, many=True)

        return Response(users.data)


class UserProfile(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    lookup_field = 'pk'
    queryset = User.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(pk=self.request.user.id)
        return obj


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"error": "Wrong password."})
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()

            return Response({'success': "Password changed successfully"})

        return Response(serializer.errors)


@method_decorator(csrf_protect, name='dispatch')
class ResetPassword(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        email = self.request.data['email']
        print("email", email)
        serializer = ResetPasswordSerializer(data=email)
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=self.request).domain
            # relative_link = reverse('reset_password_confirm', kwargs={
                                    # 'uidb64': uidb64, 'token': token})
            relative_link = f"/reset-password/{uidb64}/{token}"
            absurl = 'http://'+current_site+relative_link
            email_body = 'Hi\nUse the link below to verify your email\n' + absurl
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your email'}
            Util.send_email(data)
            return Response({'success': 'We have sent the link to reset your password'}, status.HTTP_200_OK)
        else:
            return Response({'error': "Account registered to this email does not exist"})


class PasswordTokenCheck(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, uidb64, token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid. request a new one'}, status.HTTP_400_BAD_REQUEST)
            return Response({'success': 'Credentials valid', 'uidb64': uidb64, 'token': token})

        except DjangoUnicodeDecodeError as identifier:
            return Response({'error': 'Token is not valid. request a new one'}, status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_protect, name='dispatch')
class SetNewPassword(APIView):
    permission_classes = [permissions.AllowAny]

    def put(self, request, format=None):
        serializer = SetNewPasswordSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': 'Password reset sucessful'})
