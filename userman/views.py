from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.views import LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import View  # noqa

from userman.forms import LoginForm, SignUpForm
from utils.mixins import AppFormView, AppLogoutRequiredMixin


class UserSignUpPageView(AppLogoutRequiredMixin, AppFormView):
    """View to handle the user signup."""

    form_class = SignUpForm
    template_name = "signup.html"

    def form_valid(self, form):
        """Data is valid, create user."""

        user = get_user_model().objects.create_user(**form.get_cleaned_data())
        login(self.request, user)

        return HttpResponseRedirect(
            reverse_lazy(
                "userman:user_login_page_view",
            )
        )


class UserLoginPageView(AppLogoutRequiredMixin, View):
    """View from where the user logs into the app."""

    template_name = "login.html"
    form_class = LoginForm

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        if request.GET.get("next"):
            redirect_url = request.GET.get("next")
        else:
            redirect_url = reverse("blog:homepage_view")
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(redirect_url)
        # form.er
        return render(
            request, self.template_name, {"form": form, "message": "Invalid Login"}
        )


class UserLogoutPageView(LogoutView):
    """View from the user can log out of our application."""

    pass
