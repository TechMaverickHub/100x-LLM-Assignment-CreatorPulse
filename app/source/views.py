from django.conf import settings
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView

from app.global_constants import ErrorMessage, SuccessMessage
from app.source.serializers import SourceCreateSerializer
from app.utils import get_response_schema
from permissions import IsUser


# Create your views here.
class SourceCreateAPIView(GenericAPIView):
    permission_classes = [IsUser]

    @swagger_auto_schema(
        request_body=
        openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="Source name"),
                "url": openapi.Schema(type=openapi.TYPE_STRING, description="Source url"),
                "source_type": openapi.Schema(type=openapi.TYPE_INTEGER, description="Source type"),
                "description": openapi.Schema(type=openapi.TYPE_STRING, description="Source description"),
            },
        )
    )
    def post(self, request):

        if "name" not in request.data or "url" not in request.data or "source_type" not in request.data:
            return get_response_schema(
                {settings.REST_FRAMEWORK['NON_FIELD_ERRORS_KEY']: [ErrorMessage.MISSING_FIELDS.value]},
                ErrorMessage.BAD_REQUEST.value,
                status.HTTP_400_BAD_REQUEST
            )

        request.data['user'] = request.user.id

        serializer = SourceCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return get_response_schema(serializer.data, SuccessMessage.RECORD_CREATED.value, status.HTTP_201_CREATED)

        return get_response_schema(serializer.errors, ErrorMessage.BAD_REQUEST.value, status.HTTP_400_BAD_REQUEST)
