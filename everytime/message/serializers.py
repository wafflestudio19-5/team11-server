from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import serializers, status
import common.custom_exception

from .models import Message

class MessageCreateSerializer(serializers.ModelSerializer):
    article_id = 
    comment_id = 
    class Meta:
        model =  Message
        fields = ('__all__')

    #def create(self, validated_data):
