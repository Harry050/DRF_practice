from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()

router.register('userprofile', UserViewSets)


urlpatterns = [
    path('', include(router.urls)),
    path('home/', home, name='home'),
    path('register/', register, name='register'),
    path('login/', loging_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('break/', break_view, name='break'),
    path('count/', count_view, name='count'),
    path('total/', total_view, name='total'),
    path('user_view/', user_view, name='user_view'),
    #path('apiview/', UserViewSets, name='apiview'),
]