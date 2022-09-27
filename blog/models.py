from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField

from utils.helpers import random_n_token
from utils.managers import BaseObjectManagerQuerySet
from utils.models import BaseModel

# Create your models here.


class Blog(BaseModel):
    """Blogs model"""

    title = models.CharField(_("title"), max_length=255)
    slug = models.CharField(_("slug"), max_length=255, blank=True)
    description = HTMLField(_("description"))
    author = models.ForeignKey(
        get_user_model(), related_name="blogs", on_delete=models.CASCADE
    )

    objects = BaseObjectManagerQuerySet.as_manager()

    class Meta:
        verbose_name = "blog"
        verbose_name_plural = "blogs"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) + "-" + random_n_token()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:blog_detail_view", args=[self.slug])
