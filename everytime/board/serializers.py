from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers, status
from .models import Board
from university.models import University


class BoardNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('id', 'name')


class BoardSerializer(serializers.ModelSerializer):
    university = serializers.CharField()

    class Meta:
        model = Board
        fields = ('id', 'name', 'university')

    def validate(self, data):

        # name 및 university 정보를 포함해야 함
        error = {}
        for i in ('name', 'university'):
            if i not in data:
                error[i] = "field is required"
        if error:
            raise serializers.ValidationError(error)

        # 존재하지 않는 대학
        try:
            university = University.objects.get(name=data['university'])
        except ObjectDoesNotExist:
            raise serializers.ValidationError({"status": "No such university exists"})

        # 이미 존재하는 게시판
        if len(Board.objects.filter(name=data['name'], university=university)):
            raise serializers.ValidationError({"status": "This Board has already exists in this university"})

        return data

    def create(self, validated_data):
        university = University.objects.get(name=validated_data['university'])
        board = Board.objects.create(university=university, name=validated_data['name'])
        return board
