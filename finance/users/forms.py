from django.contrib.auth.models import User
from django.forms import CharField, TextInput, PasswordInput    #, ModelForm, ImageField, FileInput
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


# from . import models
# from .models import Profile


class RegisterForm(UserCreationForm):
    username = CharField(min_length=3, max_length=25, required=True,
                         widget=TextInput(attrs={'label': 'User name:',
                                                 'placeholder': 'User name',
                                                 'class': 'col-sm-12 form-control'}))
    password1 = CharField(min_length=5, max_length=50, required=True,
                          widget=PasswordInput(attrs={'label': 'Password:',
                                                      'placeholder': 'Password',
                                                      'class': 'col-sm-12 form-control'}))
    password2 = CharField(min_length=5, max_length=50, required=True,
                          widget=PasswordInput(attrs={'label': 'Password confirm:',
                                                      'placeholder': 'Password confirm',
                                                      'class': 'col-sm-12 form-control'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = CharField(required=True,
                         widget=TextInput(attrs={'label': 'User name:',
                                                 'placeholder': 'User name',
                                                 'class': 'col-sm-12 form-control'}))
    password = CharField(required=True, widget=PasswordInput(attrs={'label': 'Password:',
                                                                    'placeholder': 'Password',
                                                                    'class': 'col-sm-12 form-control'}))

    class Meta:
        model = User
        fields = ['username', 'password']

# class ProfileForm(ModelForm):
#     avatar = ImageField(widget=FileInput())
#
#     class Meta:
#         model = Profile
#         fields = ['avatar']
