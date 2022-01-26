from rest_framework import serializers, status, viewsets, permissions
from rest_framework.response import Response
from .serializers import *
from lecture.models import *


class InformationViewSet(viewsets.GenericViewSet):
    serializer_class = InformationCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    # POST /subject_professor/{subject_professor}/information/
    def create(self, request, subject_professor_id):

        if not (subject_professor := SubjectProfessor.objects.get_or_none(id=subject_professor_id)):
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={"error": "wrong_board_id", "detail": "SubjectProfessor가 존재하지 않습니다."})

        data = request.data.copy()
        data['subject_professor'] = subject_professor_id

        serializer = InformationCreateSerializer(data=data, context={'request': request})
        valid = serializer.is_valid(raise_exception=True)
        information = serializer.save()

        return Response(status=status.HTTP_200_OK, data=InformationViewSerializer(information).data)

    # GET /subject_professor/{subject_professor}/information/
    def list(self, request, subject_professor_id):
        if not (subject_professor := SubjectProfessor.objects.get_or_none(id=subject_professor_id)):
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={"error": "wrong_board_id", "detail": "SubjectProfessor가 존재하지 않습니다."})

        informations= self.get_queryset().filter(subject_professor=subject_professor)
        page = self.paginate_queryset(informations)
        if page is not None:
            serializer = InformationViewSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="pagination fault")

    def get_queryset(self):
        queryset = Information.objects.all()
        return queryset





