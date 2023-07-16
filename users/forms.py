from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from users.models import User
from main.forms import FormStyleMixin
from django import forms

class UserForm(FormStyleMixin, UserChangeForm):

    class Meta:
        model = User
        fields = ('email', 'phone', 'country', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class UserRegisterForm(FormStyleMixin, UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')