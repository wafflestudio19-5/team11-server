from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers, status
from .models import College, Department
from university.models import University


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name')
class DepartmentCreateSerializer(serializers.ModelSerializer):
    college = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    class Meta:
        model = Department
        fields = ('id', 'name', 'college',)

    def validate(self, data):

        # 존재하지 않는 단과대
        try:
            college = College.objects.get(name=data['college'])
        except ObjectDoesNotExist:
            raise serializers.ValidationError({"status": "No such college exists"})

        # 이미 존재하는 학과
        if len(Department.objects.filter(name=data['name'], college=college)):
            raise serializers.ValidationError({"status": "This department has already exists in this college"})

        return data

    def create(self, validated_data):
        college = College.objects.get(name=validated_data['college'])
        department = Department.objects.create(college=college, name=validated_data['name'])
        return department

class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = ('id', 'name')

class CollegeCreateSerializer(serializers.ModelSerializer):
    university = serializers.CharField(required = True)
    name = serializers.CharField(required = True)
    class Meta:
        model = College
        fields = ('id', 'name', 'university',)

    def validate(self, data):

        # 존재하지 않는 대학
        try:
            university = University.objects.get(name=data['university'])
        except ObjectDoesNotExist:
            raise serializers.ValidationError({"status": "No such university exists"})

        # 이미 존재하는 단과대
        if len(College.objects.filter(name=data['name'], university=university)):
            raise serializers.ValidationError({"status": "This college has already exists in this university"})

        return data

    def create(self, validated_data):
        university = University.objects.get(name=validated_data['university'])
        college = College.objects.create(university=university, name=validated_data['name'])
        return college