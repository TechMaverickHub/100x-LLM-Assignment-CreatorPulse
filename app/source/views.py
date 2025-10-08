from django.conf import settings
from django.contrib.admin import ListFilter
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from app.core.views import CustomPageNumberPagination
from app.global_constants import ErrorMessage, SuccessMessage
from app.source.models import Source
from app.source.serializers import SourceCreateSerializer, SourceDisplaySerializer, SourceUpdateSerializer, \
    SourceListFilterDisplaySerializer
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


class SourceDetailAPIView(GenericAPIView):
    permission_classes = [IsUser]

    def get_object(self, pk):

        source_object = Source.objects.filter(pk=pk, is_active=True, user_id=self.request.user.id)
        if source_object:
            return source_object[0]
        return None

    def get(self, request, pk):

        source = self.get_object(pk)
        if not source:
            return get_response_schema({}, ErrorMessage.NOT_FOUND.value, status.HTTP_404_NOT_FOUND)

        serializer = SourceDisplaySerializer(source)
        return get_response_schema(serializer.data, SuccessMessage.RECORD_RETRIEVED.value, status.HTTP_200_OK)

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
    def patch(self, request, pk):

        source = self.get_object(pk)
        if not source:
            return get_response_schema({}, ErrorMessage.NOT_FOUND.value, status.HTTP_404_NOT_FOUND)

        serializer = SourceUpdateSerializer(source, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return get_response_schema(serializer.data, SuccessMessage.RECORD_UPDATED.value, status.HTTP_201_CREATED)

        return get_response_schema(serializer.errors, ErrorMessage.BAD_REQUEST.value, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):

        source = self.get_object(pk)
        if not source:
            return get_response_schema({}, ErrorMessage.NOT_FOUND.value, status.HTTP_404_NOT_FOUND)

        source.is_active = False
        source.save()
        return get_response_schema({}, SuccessMessage.RECORD_DELETED.value, status.HTTP_204_NO_CONTENT)


class SourceListFilter(ListAPIView):
    """Source: List-filter"""

    serializer_class = SourceListFilterDisplaySerializer
    pagination_class = CustomPageNumberPagination

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsUser]

    def get_queryset(self):

        source_queryset = Source.objects.select_related("source_type").filter(user_id=self.request.user.id, is_active=True).order_by("-updated")

        # Filter by name
        name = self.request.query_params.get("name", None)
        if name:
            source_queryset = source_queryset.filter(name__istartswith=name)

        # Filter by url
        url = self.request.query_params.get("url", None)
        if url:
            source_queryset = source_queryset.filter(url__icontains=url)

        # Filter by source type
        source_type = self.request.query_params.get("source_type", None)
        if source_type:
            source_queryset = source_queryset.filter(source_type_id=source_type)

        return source_queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("name", openapi.IN_QUERY, description="Filter by name", type=openapi.TYPE_STRING),
            openapi.Parameter("url", openapi.IN_QUERY, description="Filter by url", type=openapi.TYPE_STRING),
            openapi.Parameter("source_type", openapi.IN_QUERY, description="Filter by source type", type=openapi.TYPE_INTEGER),
        ]
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)



