from utils.forms import AppModelForm

from .models import Blog


class BlogForm(AppModelForm):
    class Meta(AppModelForm.Meta):
        fields = [
            "title",
            "cover_image",
            "description",
        ]
        model = Blog

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop("author")
        super().__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        return title
