from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Process,  Process_Thread, Process_Sub_Thread, UserProfile
from django.forms import ModelForm

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email','last_name', 'password1', 'password2']

class Process_Form(ModelForm):
    class Meta:
        model = UserProfile
        #fields = '__all__'
        fields = ['user','comment','user_process_sub_thread']
