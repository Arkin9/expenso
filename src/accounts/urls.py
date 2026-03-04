from django.urls import path
from .views import RequestOTPView, VerifyOTPView

urlpatterns = [
    path("login/", RequestOTPView.as_view(), name="request-otp"),
    path("verify/", VerifyOTPView.as_view(), name="verify-otp"),
]