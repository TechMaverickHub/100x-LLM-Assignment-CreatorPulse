from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from app.core.views import CustomPageNumberPagination
from app.mail.models import EmailLog
from app.mail.serializers import EmailLogListFilterSerializer, UserEmailListFilterSerializer
from permissions import IsSuperAdmin, IsUser


# Create your views here.
class EmailLogListFilterAPIView(ListAPIView):
    """List all email logs"""

    serializer_class = EmailLogListFilterSerializer
    pagination_class = CustomPageNumberPagination

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperAdmin]

    def get_queryset(self):

        email_queryset = EmailLog.objects.select_related("user").filter(is_active=True).order_by("-created")

        # Filter by user first name
        first_name = self.request.query_params.get("first_name", None)
        if first_name:
            email_queryset = email_queryset.filter(user__first_name__istartswith=first_name)

        # Filter by user last name
        last_name = self.request.query_params.get("last_name", None)
        if last_name:
            email_queryset = email_queryset.filter(user__last_name__istartswith=last_name)

        # Filter by user email
        email = self.request.query_params.get("email", None)
        if email:
            email_queryset = email_queryset.filter(recipient__istartswith=email)

        # filter by status
        status = self.request.query_params.get("status", None)
        if status:
            email_queryset = email_queryset.filter(status=status)

        return email_queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "first_name",
                openapi.IN_QUERY,
                description="Filter by user first name",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                "last_name",
                openapi.IN_QUERY,
                description="Filter by user last name",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                "email",
                openapi.IN_QUERY,
                description="Filter by user email",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                "status",
                openapi.IN_QUERY,
                description="Filter by email status",
                type=openapi.TYPE_STRING,
                enum=["SUCCESS", "FAILED"]
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class UserEmailListFilterAPIView(ListAPIView):
    """List all user emails"""

    serializer_class = UserEmailListFilterSerializer
    pagination_class = CustomPageNumberPagination

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsUser]

    def get_queryset(self):

        email_queryset = EmailLog.objects.select_related("user").filter(user_id=self.request.user.id, is_active=True).order_by("-created")

        # Filter by user email
        email = self.request.query_params.get("email", None)
        if email:
            email_queryset = email_queryset.filter(recipient__istartswith=email)

        # filter by status
        status = self.request.query_params.get("status", None)
        if status:
            email_queryset = email_queryset.filter(status=status)

        return email_queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "email",
                openapi.IN_QUERY,
                description="Filter by user email",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                "status",
                openapi.IN_QUERY,
                description="Filter by email status",
                type=openapi.TYPE_STRING,
                enum=["SUCCESS", "FAILED"]
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

