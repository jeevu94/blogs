import contextlib

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin, FormView
from werkzeug.exceptions import NotFound  # noqa


def get_model_name(model):
    """Returns the model name from the model. Used in admin dashboard."""

    if hasattr(model, "get_model_name"):
        return model.get_model_name()
    else:
        return model.__name__


class AppViewMixin:
    """
    The apps base View class. This is inherited by all the views in the application.
    Basically implements methods like getting user and other DRY stuff.

    This is similar to the `django.views.generic.base.View`.
    """

    get_object_model = None

    def get_request(self):
        return self.request

    def get_user(self):
        """Gets the current user."""

        return self.request.user

    def get_authenticated_user(self, fallback=None):
        """Returns the logged in user else None."""

        user = self.get_user()
        return user if user and user.is_authenticated else fallback

    def get_object(self, exception=NotFound, identifier="pk"):
        """
        Suppose you want to list data based on other model. This
        is a centralized function to do the same.
        """

        if self.get_object_model:
            _object = self.get_object_model.objects.get_or_none(
                **{identifier: self.kwargs[identifier]}
            )

            if not _object:
                raise exception

            return _object

        return super().get_object()

    def get_context_data(self, **kwargs):
        """
        Overridden to send model and object related data to the frontend.
        Used for dynamic stuff on the administration/dynamic/* files.
        """

        data = super().get_context_data(**kwargs)
        form_class = getattr(self, "form_class", None)

        with contextlib.suppress(ImproperlyConfigured, AttributeError):
            if hasattr(self, "get_queryset"):
                data["model_name"] = get_model_name(model=self.get_queryset().model)

        if (
            form_class
            and hasattr(form_class, "Meta")
            and hasattr(form_class.Meta, "model")
        ):
            model = form_class.Meta.model
            if model:
                data["model_name"] = get_model_name(model=model)

        if getattr(self, "object", None):
            data["object_name"] = self.object.__str__()

        return data


class AppFormMixin(AppViewMixin, FormMixin):
    """
    Contains the common methods and variables for tne FormView, and other ModelForm views.

    The django form views does not pass the request to the Form layer. This solves the
    purpose and also implements the other common methods.
    """

    def get_context_data(self, **kwargs):
        """Overridden to set the form submit path to the FE."""

        data = super().get_context_data(**kwargs)

        # next url
        _next_url = self.request.GET.get(REDIRECT_FIELD_NAME, None)
        # form submit url
        _form_submit_path = self.request.path
        # finalized url
        if _next_url:
            _form_submit_path = f"{_form_submit_path}?{REDIRECT_FIELD_NAME}={_next_url}"

        data["form_submit_action_path"] = _form_submit_path

        return data

    def get_form_kwargs(self):
        """Pass request and view."""

        kwargs = super().get_form_kwargs()
        kwargs.update(
            {
                "context": {
                    "request": getattr(self, "request", None),
                    "view": self,
                }
            }
        )
        return kwargs


class AppFormView(AppFormMixin, FormView):
    """Apps FormView. Implements some other common methods."""

    success_url = "."


class AppLogoutRequiredMixin(AccessMixin):
    """
    Allows the user to access only when he is logged out. Example
    consider the login page, forgot password page etc.

    If logged in, this redirects to the dashboard.
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated:
            return redirect(reverse_lazy(settings.LOGIN_REDIRECT_URL))
        return super().dispatch(request, *args, **kwargs)
