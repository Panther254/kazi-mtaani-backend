from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.contrib.auth import get_user_model
User = get_user_model()


# Create your views here.
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

		if password == re_password:
			if User.objects.filter(email=email).exists():
				return Response({'error': 'Email is already registered.'})
			if User.objects.filter(national_id=national_id).exists():
				return Response({'error': 'The National ID is already registred'})

			user = User.objects.create_user(email=email,password=password,first_name=first_name,last_name=last_name,phone_number=phone_number,residence=residence,national_id=national_id)
			user.save()
			content = {"Success": "User created sucessfully."}
			return Response(content, status=status.HTTP_201_CREATED)
		else:
			return Response({'error': 'Passwords do not match.'})



@method_decorator(ensure_csrf_cookie,name='dispatch')
class GetCSRFToken(APIView):
	permission_classes = [permissions.AllowAny]


	def get(self,request,format=None):
		return Response({"Success": "Token cookie has been sucessfully set"})