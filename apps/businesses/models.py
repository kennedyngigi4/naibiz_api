import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from apps.accounts.models import User
from apps.malls.models import *



# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    price = models.PositiveIntegerField()
    active_days = models.PositiveIntegerField(null=True)
    is_free = models.BooleanField(default=False)
    is_main = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    icon = models.TextField(null=True)


    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class SubLevelCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


def BusinessImagePath(instance, filename):
    user_slug = str(instance.created_by.slug)
    return f"users/{user_slug}/businesses/{filename}"


class Business(models.Model):
    SECTION_CHOICES = [
        ("featured", "Featured"),
        ("popular", "Popular"),
        ("environs", "Nairobi Environs"),
        ("new", "New"),
        ("top", "Top"),
    ]

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    slug = models.SlugField(unique=True)

    name = models.CharField(max_length=255, verbose_name=_("business name"))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name="businesses", verbose_name=_("related categories"))
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("subcategory"))
    mall = models.ForeignKey(Mall, on_delete=models.SET_NULL, null=True, related_name="business_malls")
    services = models.TextField(null=True, verbose_name=_("services"))
    location = models.CharField(max_length=255, null=True, verbose_name=_("geo location"))
    latitude = models.DecimalField(max_digits=16, decimal_places=12, null=True, verbose_name=_("latitude"))
    longitude = models.DecimalField(max_digits=16, decimal_places=12, null=True, verbose_name=_("longitude"))
    description = models.TextField(null=True, verbose_name=_("description"))

    email = models.EmailField(verbose_name=_("email"), null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, verbose_name=_("phone"))
    website = models.URLField(verbose_name=_("website link"), null=True, blank=True)

    whatsapp = models.URLField(verbose_name=_("whatsapp link"), null=True, blank=True)
    facebook = models.URLField(verbose_name=_("facebook link"), null=True, blank=True)
    instagram = models.URLField(verbose_name=_("instagram link"), null=True, blank=True)
    twitterx = models.URLField(verbose_name=_("twitter_x link"), null=True, blank=True)
    linkedin = models.URLField(verbose_name=_("linkedin link"), null=True, blank=True)
    tiktok = models.URLField(verbose_name=_("tiktok link"), null=True, blank=True)
    youtube = models.URLField(verbose_name=_("youtube link"), null=True, blank=True)

    main_banner = models.ImageField(upload_to=BusinessImagePath, null=True, blank=True, verbose_name=_("main banner"))
    profile_image = models.ImageField(upload_to=BusinessImagePath, null=True, blank=True, verbose_name=_("profile image"))
    section = models.CharField(
        max_length=20, choices=SECTION_CHOICES, null=True, blank=True,
        help_text="Used to categorize businesses in homepage sections"
    )

    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    views = models.PositiveIntegerField(default=0)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            # categories = "_ ".join([cat.name for cat in self.category.all()])
            base_slug = slugify(f"{self.name}-{self.category.name}")
            unique_suffix = uuid.uuid4().hex[:10]
            self.slug = f"{base_slug}-{unique_suffix}"

        super().save(*args, **kwargs)


    def get_week_schedule(self):
        return {
            hour.day: {
                "open": None if hour.is_closed else str(hour.opening_time),
                "close": None if hour.is_closed else str(hour.closing_time),
                "is_closed": hour.is_closed
            } for hour in self.hours.all()
        }
    

    def __str__(self):
        return f"{self.name} by {self.created_by.fullname}"


def BusinessDocsPath(instance, filename):
    user_slug = str(instance.created_by.slug)
    return f"users/{user_slug}/businesses/documents/{filename}"


class BusinessKYCData(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True, verbose_name=_("unique ID"))
    business = models.OneToOneField(Business, on_delete=models.CASCADE, related_name="kycdata", verbose_name=_("business"))

    registration_form = models.FileField(upload_to=BusinessDocsPath, null=True, blank=True)
    mpesa_settlement_number = models.CharField(max_length=20)

    def __str__(self):
        return f"KYC Data for {self.business.name}"



class BusinessHour(models.Model):

    DAY_CHOICES = [
        ( 'Mon', 'Monday', ),
        ( 'Tue', 'Tuesday', ),
        ( 'Wed', 'Wednesday', ),
        ( 'Thu', 'Thursday', ),
        ( 'Fri', 'Friday', ),
        ( 'Sat', 'Saturday', ),
        ( 'Sun', 'Sunday', ),
    ]

    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="hours")
    day = models.CharField(max_length=4, choices=DAY_CHOICES)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)
    


    class Meta:
        unique_together = ( 'business', 'day')

    def __str__(self):
        return f"{self.business.name} - {self.day}"



class BusinessGallery(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="gallery")
    image = models.ImageField(upload_to=BusinessImagePath)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.business.name}"



class Review(models.Model):

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True, verbose_name=_("unique ID"))
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="reviews", verbose_name=_("business"))

    email = models.EmailField(verbose_name=_("email"))
    rating = models.PositiveIntegerField(verbose_name=_("rating"))
    title = models.CharField(max_length=255, verbose_name=_("title"))
    message = models.TextField(verbose_name=_("message"))
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.title} rating for {self.business.name}"



