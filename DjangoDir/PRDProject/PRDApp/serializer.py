from rest_framework import serializers
from .models import *


class Serializers_Process(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = ('id', 'process_name')

class Serializers_Process_Thread(serializers.ModelSerializer):
    class Meta:
        model = Process_Thread
        fields = ('id', 'process_thread_name')

class Serializers_Process_Sub_Thread(serializers.ModelSerializer):
    class Meta:
        model = Process_Sub_Thread
        fields = ('id', 'process_sub_thread_name')


class Serializers_Process_Sub_Thread_List(serializers.ModelSerializer):
    queryset = serializers.PrimaryKeyRelatedField(queryset=Process_Sub_Thread.objects.all(), many=True)
    class Meta:
        model = UserProfile
        fields = ('user', 'comment', 'date_created', 'user_process_thread', 'queryset')

class Serializers_UserProfile(serializers.ModelSerializer):
    tag = Serializers_Process_Sub_Thread_List(read_only= True, many= True)
    class Meta:
        model = UserProfile
        fields = ('user', 'comment', 'date_created', 'user_process_thread','user_process_sub_thread','tag')



class Serializers_ManyUserProfile(serializers.ModelSerializer):
    tracks = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ('username','tracks')
