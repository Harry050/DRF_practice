from rest_framework.utils import field_mapping
from .models import Articles
from rest_framework import serializers


class Articles_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = ['title','author','emails']

