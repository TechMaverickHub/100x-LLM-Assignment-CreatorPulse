from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from app.core.views import CustomPageNumberPagination
from app.global_constants import SuccessMessage, ErrorMessage
from app.sample.models import UserStyleSample
from app.sample.serializers import UserStyleSampleCreateSerializer, UserStyleSampleDisplaySerializer, \
    UserStyleSampleUpdateSerializer
from app.utils import get_response_schema
from permissions import IsUser


# Create your views here.
class UserStyleSampleCreateAPIView(GenericAPIView):
    """View for creating a user style sample"""

    permission_classes = [IsUser]

    @swagger_auto_schema(
        request_body=
        openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "text": openapi.Schema(type=openapi.TYPE_STRING, description="Text sample"),
            },
        )
    )
    def post(self, request):
        request.data["user"] = request.user.id

        serializer = UserStyleSampleCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return get_response_schema(serializer.data, SuccessMessage.RECORD_CREATED.value, status.HTTP_201_CREATED)

        return get_response_schema(serializer.errors, ErrorMessage.BAD_REQUEST.value, status.HTTP_400_BAD_REQUEST)


class UserStyleSampleDetailAPIView(GenericAPIView):
    """View for retrieving, updating, and deleting a user style sample"""

    permission_classes = [IsUser]

    def get_object(self, request, pk):
        user_style_sample = UserStyleSample.objects.filter(pk=pk, user_id=request.user.id, is_active=True)
        if not user_style_sample:
            return None
        return user_style_sample.first()

    def get(self, request, pk):
        user_style_sample = self.get_object(request, pk)

        if not user_style_sample:
            return get_response_schema({}, ErrorMessage.NOT_FOUND.value, status.HTTP_404_NOT_FOUND)

        serializer = UserStyleSampleDisplaySerializer(user_style_sample)

        return get_response_schema(serializer.data, SuccessMessage.RECORD_RETRIEVED.value, status.HTTP_200_OK)


    @swagger_auto_schema(
        request_body=
        openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "text": openapi.Schema(type=openapi.TYPE_STRING, description="Text sample"),
            },
        )
    )


    def patch(self, request, pk):
        user_style_sample = self.get_object(request, pk)

        if not user_style_sample:
            return get_response_schema({}, ErrorMessage.NOT_FOUND.value, status.HTTP_404_NOT_FOUND)

        serializer = UserStyleSampleUpdateSerializer(user_style_sample, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return get_response_schema(serializer.data, SuccessMessage.RECORD_UPDATED.value, status.HTTP_200_OK)
        return get_response_schema(serializer.errors, ErrorMessage.BAD_REQUEST.value, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user_style_sample = self.get_object(request, pk)

        if not user_style_sample:
            return get_response_schema({}, ErrorMessage.NOT_FOUND.value, status.HTTP_404_NOT_FOUND)

        user_style_sample.is_active = False
        user_style_sample.save()

        return get_response_schema({}, SuccessMessage.RECORD_DELETED.value, status.HTTP_204_NO_CONTENT)


class UserStyleSampleListFilterAPIView(ListAPIView):

    serializer_class = UserStyleSampleDisplaySerializer
    pagination_class = CustomPageNumberPagination

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsUser]

    def get_queryset(self):

        user_style_samples = UserStyleSample.objects.filter(user_id=self.request.user.id, is_active=True).order_by("-updated")

        return user_style_samples

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

