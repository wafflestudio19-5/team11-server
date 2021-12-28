from re import U
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import serializers, status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import *
from university.models import University
#from .models import Article

# Create your views here.
class ArticleViewSet(viewsets.GenericViewSet):
    pass