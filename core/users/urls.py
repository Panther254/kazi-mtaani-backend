from django.urls import path,include
from .views import SignUpView, GetCSRFToken, LoginView, LogoutView, CheckAuthenticated, DeleteAccountView, GetUsersView, UserProfile, ChangePasswordView, ResetPassword, PasswordTokenCheck, SetNewPassword

urlpatterns = [
	path('register', SignUpView.as_view()),
	path('login', LoginView.as_view()),
	path('logout', LogoutView.as_view()),
	path('authenticated', CheckAuthenticated.as_view()),
	path('get-cookie', GetCSRFToken.as_view()),
	path('delete-user', DeleteAccountView.as_view()),
	path('get-users', GetUsersView.as_view()),
	path('profile', UserProfile.as_view()),
	path('change-password', ChangePasswordView.as_view()),
	path('reset-password', ResetPassword.as_view(),name='reset_password'),
	path('reset-password-confirm/<uidb64>/<token>/', PasswordTokenCheck.as_view(),name='reset_password_confirm'),
	path('reset-password-complete', SetNewPassword.as_view(),name='reset_password_complete'),
]