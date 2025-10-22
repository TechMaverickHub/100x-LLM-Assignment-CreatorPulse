from django.urls import path

from app.credit.views import CreditDetailAPIView

urlpatterns = [
    # Authentication
    path("", CreditDetailAPIView.as_view(), name="credit-detail"),

]
