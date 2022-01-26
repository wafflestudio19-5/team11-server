from django.utils import timezone
from rest_framework import serializers
from .models import University
from department.models import Department

class UniversitySerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    class Meta:
        model = University
        fields = ('name', 'email',)

    def validate(self, data):
        error = {}
        for i in ('name', 'email'):
            if i not in data:
                error[i] = "field is required"
        if error:
            raise serializers.ValidationError(error)

        return data
    def create(self, validated_data):
        university = University.objects.create(name=validated_data['name'], email_domain=validated_data['email'])
        return university

class UniversityViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = University
        fields = ('id', 'name',)

