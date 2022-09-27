from django.http import HttpResponseRedirect
from django.urls import reverse

from blog.forms import BlogForm
from blog.models import Blog
from utils.mixins import (
    AppAdminTypeOnlyAllowedMixin,
    AppCreateView,
    AppDetailView,
    AppListView,
    AppLoginRequiredMixin,
    AppUpdateView,
)


class BlogsView(AppLoginRequiredMixin, AppListView):
    template_name = "homepage.html"
    queryset = Blog.objects.select_related("author").order_by("-updated_at")
    context_object_name = "blogs"


class DetailBlogView(AppLoginRequiredMixin, AppDetailView):
    model = Blog
    queryset = Blog.objects.select_related("author").all()
    template_name = "blog.html"
    context_object_name = "blog"
    slug_field = "slug"


class CreateBlogView(AppAdminTypeOnlyAllowedMixin, AppCreateView):
    template_name = "blog_create.html"
    form_class = BlogForm

    def form_valid(self, form):
        """Data is valid, create blog."""

        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(
            reverse("blog:blog_detail_view", args=[self.object.slug])
        )

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs()
        kwargs["author"] = self.request.user
        return kwargs


class UpdateBlogView(AppAdminTypeOnlyAllowedMixin, AppUpdateView):
    template_name = "blog_create.html"
    form_class = BlogForm
    model = Blog
    queryset = Blog.objects.select_related("author").all()
    context_object_name = "blog"
    slug_field = "slug"

    def get_success_url(self):
        return reverse("blog:blog_detail_view", args=(self.object.slug,))

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs()
        kwargs["author"] = self.request.user
        return kwargs
