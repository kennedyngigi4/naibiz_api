import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.core.exceptions import ValidationError

from apps.accounts.models import *
from apps.businesses.models import *
# Create your models here.


def ProductImagePath(instance, filename):
    user_slug = str(instance.business.created_by.slug)
    return f"users/{user_slug}/businesses/products/{filename}"


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, verbose_name=_("unique ID"))
    name = models.CharField(max_length=255, verbose_name=_("name"))
    slug = models.SlugField(unique=True, verbose_name=_("slug"))

    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, verbose_name=_("categories"))
    main_image = models.ImageField(upload_to=ProductImagePath, verbose_name=_("image"))
    description = models.TextField(verbose_name=_("description"))

    price = models.PositiveIntegerField(verbose_name=_("price"))
    discounted_price = models.PositiveIntegerField(verbose_name=_("discounted price "), null=True, blank=True)
    is_discounted = models.BooleanField(default=False)
    in_stock = models.BooleanField(default=True)

    business = models.ForeignKey(Business, related_name="products", on_delete=models.CASCADE, verbose_name=_("related business"))
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("owner"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("time created"))


    @property
    def is_active(self):
        if self.business.is_active:
            return True
        return False
    
    
    def clean(self):
        if self.is_discounted and self.discounted_price:
            if self.discounted_price >= self.price:
                raise ValidationError("Discounted price must be less than original price.")


    def save(self, *args, **kwargs):
        # self.clean()

        if not self.slug:
            base_slug = slugify(self.name)
            unique_suffix = uuid.uuid4().hex[:10]
            self.slug = f"{base_slug}-{unique_suffix}"
        
        super().save(*args, **kwargs)

    class Meta:
        ordering = [ '-created_by' ]


    def __str__(self):
        return f"{self.name} of {self.business.name} owned by {self.created_by.fullname}"

