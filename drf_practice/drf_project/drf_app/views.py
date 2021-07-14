from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.views.decorators import csrf
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from .models import Articles
from .serializers import Articles_Serializer
# Create your views here.

@csrf_exempt
def articles_list(requets):

    if requets.method == 'GET':
        articles = Articles.objects.all()
        serializer_data = Articles_Serializer(articles, many = True)
        return JsonResponse(serializer_data.data, safe=False)

    elif requets.method == 'POST':
        data = JSONParser().parse(requets)
        serializer = Articles_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status = 400)


@csrf_exempt
def articles_details(request, pk):
    try:
        articles_data = Articles.objects.get(pk=pk)
    except Articles.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer_details = Articles_Serializer(articles_data)
        return JsonResponse(serializer_details.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializers = Articles_Serializer(articles_data, data=data)
        if serializers.is_valid():
            serializers.save()
            return JsonResponse(serializers.data)
        return JsonResponse(serializers.errors, status=400)
    elif request.method == 'DELETE':
        articles_data.delete()
        return HttpResponse(status=204)