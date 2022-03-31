from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status, generics
from django.contrib import auth
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.contrib.auth import get_user_model
User = get_user_model()
from .serializers import UserSerializer, UserProfileSerializer


# Create your views here.
@method_decorator(csrf_protect, name='dispatch')
class CheckAuthenticated(APIView):
	def get(self, request, format=None):
		is_authenticated = User.is_authenticated
		if is_authenticated:
			return Response({'is_authenticated': 'Success'})
		else:
			return Response({'is_authenticated': 'Error'})



@method_decorator(csrf_protect, name='dispatch')
class SignUpView(APIView):
	permission_classes = [permissions.AllowAny]

	def post(self, request, format=None):
		data = self.request.data

		first_name = data['first_name']
		last_name = data['last_name']
		email = data['email']
		phone_number = data['phone_number']
		residence = data['residence']
		national_id = data['national_id']
		password = data['password']
		re_password = data['re_password']

		try:
			if password == re_password:
				if User.objects.filter(email=email).exists():
					return Response({'error': 'Email is already registered.'})
				if User.objects.filter(national_id=national_id).exists():
					return Response({'error': 'The National ID is already registred'})

				user = User.objects.create_user(email=email,password=password,first_name=first_name,last_name=last_name,phone_number=phone_number,residence=residence,national_id=national_id)
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

	def post(self,request,format=None):
		data = self.request.data

		email = data['email']
		password = data['password']

		try:
			user = auth.authenticate(email=email,password=password)
			if user is not None:
				auth.login(request,user)
				return Response({'success': 'Login sucessful'}, status=status.HTTP_202_ACCEPTED)
			else:
				return Response({'error': 'Error logging in'}, status=status.HTTP_406_NOT_ACCEPTABLE)
		except:
			return Response({'error': 'Something went wrong'})

class LogoutView(APIView):
	def post(self,request,format=None):
		try:
			auth.logout(request)
			return Response({'success': 'Logging out sucessful'})
		except:
			return Response({'error': 'Something went wrong when logging out'})

@method_decorator(ensure_csrf_cookie,name='dispatch')
class GetCSRFToken(APIView):
	permission_classes = [permissions.AllowAny]


	def get(self,request,format=None):
		return Response({"success": "Token cookie has been sucessfully set"})


class DeleteAccountView(APIView):
	def delete(self,request,format=None):
		user = self.request.user
		try:
			user = User.objects.filter(id=user.id).delete()
			return Response({'success': 'User deleted sucessfully'})
		except:
			return Response({'error': 'Something went wrong trying to delete user'})

class GetUsersView(APIView):
	permission_classes = [permissions.AllowAny]

	def get(self,request,format=None):
		users = User.objects.all()

		users = UserSerializer(users,many=True)

		return Response(users.data)



class UserProfile(generics.RetrieveUpdateAPIView):
	serializer_class = UserProfileSerializer
	lookup_field = 'pk'
	queryset = User.objects.all()
	
	def get_object(self):
		queryset = self.filter_queryset(self.get_queryset())
		obj = queryset.get(pk=self.request.user.id)
		return obj
