from django import forms
from django.contrib.auth import get_user_model, password_validation

from utils.forms import AppModelForm


def app_clean_password(password):
    """App's function to validate password."""

    password_validation.validate_password(password, None)
    return password


class SignUpForm(AppModelForm):
    class Meta(AppModelForm.Meta):
        fields = [
            "first_name",
            "last_name",
            "email",
            "password",
        ]
        model = get_user_model()
        widgets = {"password": forms.PasswordInput}

    def clean_password(self):
        """Password validations."""

        return app_clean_password(self.get_cleaned_data("password"))


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100, required=True)
    password = forms.CharField(
        widget=forms.PasswordInput, max_length=100, required=True
    )
