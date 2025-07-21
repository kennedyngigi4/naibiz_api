import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from apps.accounts.models import *
from apps.businesses.models import *
# Create your models here.


def BlogImagePath(instance, filename):
    user_slug = str(instance.author.slug)
    return f"users/{user_slug}/blogs/{filename}"


class Blog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, verbose_name=_("unique ID"))
    slug = models.SlugField(unique=True, verbose_name=_("slug"))

    title = models.CharField(max_length=255, verbose_name=_("title"))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, verbose_name=_("categories"))
    content = models.TextField(verbose_name=_("content"))
    image = models.ImageField(upload_to=BlogImagePath)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)
    for_company = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_suffix = uuid.uuid4().hex[:10]
            self.slug = f"{base_slug}-{unique_suffix}"
        super().save(*args, **kwargs)


    def __str__(self):
        return str(self.title)


