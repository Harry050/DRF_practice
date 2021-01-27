from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CreateUserForm, Process_Form
# Create your views here.
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from .models import Process, Process_Thread, UserProfile, Process_Sub_Thread
from django.contrib.auth.models import User

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import Serializers_Process, Serializers_Process_Thread, Serializers_Process_Sub_Thread, Serializers_UserProfile, Serializers_ManyUserProfile
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import viewsets


class UserViewSets(viewsets.ModelViewSet):
    queryset = UserProfile.objects.filter(id=2)
    serializer_class = Serializers_UserProfile
    

@api_view(['GET'])
def user_view(request):
    user_data = User.objects.filter(username='harish')
    
    serializer = Serializers_ManyUserProfile(user_data, many=True)
    return Response(serializer.data)


@login_required(login_url='login')
def home(request):
    if request.method == 'POST':
            comments = request.POST.get('textareaid')
            process = request.POST.get('process_value')
            thread = request.POST.get('thread_value')
            sub_thread = request.POST.get('sub_thread_value')

            process_id = Process.objects.get(process_name=process)
            thread_id = Process_Thread.objects.get(process_thread_name=thread,process=process_id.id)

            sub_thread_id = Process_Sub_Thread.objects.get(process_sub_thread_name=sub_thread)

            order = UserProfile(user=request.user, comment= comments, user_process=process_id, user_process_thread=thread_id)
            order.save()
            order.user_process_sub_thread.add(sub_thread_id)
            order.save()

    return render(request, 'home.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('login')

        context = {'form': form}
        return render(request, 'register.html', context)

def loging_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')        
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or Password is incorrect')

        context = {}
        return render(request, 'login.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')


def break_view(request):
    context = {}
    return render(request, 'break_page.html', context)


def count_view(request):
    if request.method == 'GET':
        user_data = UserProfile.objects.filter(user=4)
        context = {'user_data': user_data}
        return render(request, 'count_page.html', context)


def total_view(request):
    context = {}
    return render(request, 'total_page.html', context)