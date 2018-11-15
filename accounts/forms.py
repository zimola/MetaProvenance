from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()


class SignUpForm(forms.ModelForm):
    pass


class SignInForm(forms.Form):
    pass
