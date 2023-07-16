from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from users.views import ProfileUpdateView, RegisterView, activate_user, generate_pass
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [

    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<email>/', activate_user, name='activate'),
    path('backup_pass', generate_pass, name='generate_password'),

]