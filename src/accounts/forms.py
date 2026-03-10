from django import forms

class EmailForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control form-control-user',
                'placeholder': 'Enter Email Address...',
                'autocomplete': 'email',
            }
        )
    )


class OTPForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        min_length=6,
        required=True,
        widget=forms.HiddenInput(),
        error_messages={
            'required': 'Please enter the 6-digit OTP',
            'min_length': 'OTP must be 6 digits',
            'max_length': 'OTP must be 6 digits',
        }
    )

    def clean_otp(self):
        data = self.cleaned_data['otp']
        if not data.isdigit():
            raise forms.ValidationError("OTP must contain only digits.")
        return data