from audioop import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, CreateView
from django.contrib.auth.views import PasswordResetView
from config import settings
from users.models import User
from django.urls import reverse_lazy
from users.forms import UserForm, UserRegisterForm
from users.services import confirm_account
from django.shortcuts import redirect, render
from django.contrib.auth.base_user import BaseUserManager
from django.core.mail import send_mail


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('main:homepage')

    def form_valid(self, form):
        self.object = form.save()
        self.object.is_active = False
        confirm_account(self.object)
        self.object.save()
        return super().form_valid(form)

    # def get_success_url(self):
    #     url_1 = super().get_success_url()
    #     return str(url_1) + str(self.object.email)


def activate_user(request, email):
    user = User.objects.filter(email=email).first()
    user.is_active = True
    user.save()
    return redirect('users:login')


def generate_pass_f(email):
    p = BaseUserManager()
    new_pass = p.make_random_password()
    print(new_pass)
    user = User.objects.filter(email=email).first()
    send_mail(
        subject='Восстановление пароля',
        message=f'Ваш новый пароль {new_pass}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email]
    )
    user.set_password(new_pass)
    user.save()


def generate_pass(request):
    if request.method == "POST":
        email = request.POST.get('email')
        generate_pass_f(email)

    return render(request, 'users/backup_pass.html')



