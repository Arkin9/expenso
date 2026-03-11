from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import RequestOTPView, VerifyOTPView, UserLogoutView

app_name = "accounts"

urlpatterns = [
    path("login/", RequestOTPView.as_view(), name="request_otp"),
    path("verify/", VerifyOTPView.as_view(), name="verify_otp"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)