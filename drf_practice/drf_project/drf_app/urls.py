from django.urls import path
from .views import articles_list, articles_details

urlpatterns = [
    path('article/', articles_list),
    path('details/<int:pk>/', articles_details),
]
