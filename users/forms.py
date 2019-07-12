from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(UserCreationForm):
    email= forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'password']

    def clean_email(self):
        email=self.cleaned_data.get('email')
        if not "" in email:
            raise forms.ValidationError("Please enter gmail id")
        return email