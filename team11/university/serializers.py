from django.utils import timezone
from rest_framework import serializers
from .models import University
from department.serializers import DepartmentNameSerializer
from department.models import Department

class UniversitySerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    class Meta:
        model = University
        fields = ('name', 'email')

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

    departments = serializers.SerializerMethodField()

    class Meta:
        model = University
        fields = ('id', 'name', 'email_domain', 'departments')

    def get_departments(self, instance):
        return DepartmentNameSerializer(instance.university_departments.filter(), many=True).data


