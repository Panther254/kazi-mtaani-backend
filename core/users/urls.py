from django.urls import path
from .views import SignUpView, GetCSRFToken, LoginView, LogoutView, CheckAuthenticated, DeleteAccountView, GetUsersView, UserProfile

urlpatterns = [
	path('register', SignUpView.as_view()),
	path('login', LoginView.as_view()),
	path('logout', LogoutView.as_view()),
	path('authenticated', CheckAuthenticated.as_view()),
	path('get-cookie', GetCSRFToken.as_view()),
	path('delete-user', DeleteAccountView.as_view()),
	path('get-users', GetUsersView.as_view()),
	path('profile', UserProfile.as_view()),
]