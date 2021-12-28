# from django.core.exceptions import ObjectDoesNotExist
# from rest_framework import serializers, status
# from .models import Board
# from university.models import University





# class BoardSerializer(serializers.ModelSerializer):
#     name = serializers.CharField(required=True)
#     university = serializers.CharField()
#     type = serializers.ChoiceField(choices = Board.BoardType.choices)
#     description = serializers.CharField(allow_blank =True)
#     allow_anonymous = serializers.BooleanField()

#     class Meta:
#         model = Board
#         fields = ('id', 'name', 'university', 'type', 'description', 'allow_anonymous')

#     def validate(self, data):

#         # 존재하지 않는 대학
#         try:
#             university = University.objects.get(name=data['university'])
#         except ObjectDoesNotExist:
#             raise serializers.ValidationError({"detail": "No such university exists"})

#         # 이미 존재하는 게시판
#         if len(Board.objects.filter(name=data['name'], university=university)):
#             raise serializers.ValidationError({"detail": "This Board has already exists in this university"})

#         return data


#     def create(self, validated_data):
#         validated_data['university'] = University.objects.get(name=validated_data['university'])
#         board = Board.objects.create(**validated_data)
#         return board
        
# class BoardNameSerializer(BoardSerializer):
#     university = serializers.SerializerMethodField()
#     class Meta(BoardSerializer.Meta):
#         pass
    
#     def get_university(self, obj):
#         return obj.university.name

# class BoardGetSeriallizer(serializers.ModelSerializer):
#     name = serializers.CharField()
#     type = serializers.ChoiceField(choices=Board.BoardType.choices)
#     description = serializers.CharField()

#     class Meta:
#         model = Board
#         fields = ('id', 'name', 'type', 'description')

# class BoardFilteredSerializer(serializers.ModelSerializer):
#     name = serializers.CharField()
#     description = serializers.CharField()

#     class Meta:
#         model = Board
#         fields = ('id', 'name', 'description')

