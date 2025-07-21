import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from apps.accounts.models import User
# Create your models here.



def MallImagePath(instance, filename):
    user_slug = str(instance.created_by.slug)
    return f"users/{user_slug}/malls/{filename}"


class Mall(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, verbose_name=_("unique ID"))
    name = models.CharField(max_length=255, verbose_name=_("name"))
    slug = models.SlugField(unique=True)

    main_image = models.ImageField(upload_to=MallImagePath, verbose_name=_("image"))
    floors = models.PositiveIntegerField(verbose_name=_("floors number"))
    stalls = models.PositiveIntegerField(verbose_name=_("stalls"))
    descriprion = models.TextField(verbose_name=_("description"))

    phone = models.CharField(max_length=20, verbose_name=_("phone"))
    email = models.EmailField(verbose_name=_("email address"))
    website = models.URLField(verbose_name=_("website link"), blank=True, null=True)

    whatsapp = models.URLField(verbose_name=_("whatsapp link"), null=True, blank=True)
    facebook = models.URLField(verbose_name=_("facebook link"), null=True, blank=True)
    instagram = models.URLField(verbose_name=_("instagram link"), null=True, blank=True)
    twitter_x = models.URLField(verbose_name=_("twitter_x link"), null=True, blank=True)
    linkedin = models.URLField(verbose_name=_("linkedin link"), null=True, blank=True)
    tiktok = models.URLField(verbose_name=_("tiktok link"), null=True, blank=True)
    youtube = models.URLField(verbose_name=_("youtube link"), null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            unique_suffix = uuid.uuid4().hex[:10]
            self.slug = f"{base_slug}-{unique_suffix}"
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.name} by {self.created_by.fullname}"




