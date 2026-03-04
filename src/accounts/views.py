from django.views.generic.edit import FormView
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from .models import User, EmailOTP
from .forms import EmailForm, OTPForm


class RequestOTPView(FormView):
    template_name = "accounts/request_otp.html"
    form_class = EmailForm

    def form_valid(self, form):
        email = form.cleaned_data["email"]

        user, created = User.objects.get_or_create(email=email)

        otp_code = EmailOTP.generate_otp()

        EmailOTP.objects.create(
            user=user,
            otp=otp_code
        )

        send_mail(
            "Your Expenso Login OTP",
            f"Your OTP is {otp_code}",
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )

        self.request.session["otp_user_id"] = user.id

        messages.success(self.request, "OTP sent to your email.")

        return redirect("verify-otp")



class VerifyOTPView(FormView):
    template_name = "accounts/verify_otp.html"
    form_class = OTPForm

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get("otp_user_id"):
            return redirect("request-otp")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        otp_input = form.cleaned_data["otp"]
        user_id = self.request.session.get("otp_user_id")

        try:
            otp_obj = EmailOTP.objects.filter(
                user_id=user_id,
                is_verified=False
            ).latest("created_at")
        except EmailOTP.DoesNotExist:
            messages.error(self.request, "No OTP found. Please try again.")
            return redirect("request-otp")

        # Expiry check (5 min)
        if (timezone.now() - otp_obj.created_at).seconds > 300:
            messages.error(self.request, "OTP expired.")
            return redirect("request-otp")

        # Attempt limit
        if otp_obj.attempts >= 5:
            messages.error(self.request, "Too many attempts.")
            return redirect("request-otp")

        if otp_obj.otp == otp_input:
            otp_obj.is_verified = True
            otp_obj.save()

            login(self.request, otp_obj.user)

            del self.request.session["otp_user_id"]

            messages.success(self.request, "Login successful 🎉")

            return redirect("dashboard")

        else:
            otp_obj.attempts += 1
            otp_obj.save()

            messages.error(self.request, "Invalid OTP.")

            return redirect("verify-otp")