from django import forms
from django.forms import ModelForm

from .models import AdvUser, Poll
from django.contrib.auth.forms import UserCreationForm


class ChangeUserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True,
                             label='Адрес электронной почты')

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'first_name', 'last_name', 'avatar')


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'password1', 'password2', 'avatar')

