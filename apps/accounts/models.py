import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, fullname, phone, password, **extra_fields):

        if not email:
            raise ValueError(_("Email is required"))
        
        if not fullname:
            raise ValueError(_("Full name is required"))
        
        if not phone:
            raise ValueError(_("Phone is required"))
        

        user = self.model(
            email=self.normalize_email(email).lower(),
            fullname=fullname,
            phone=phone,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self, email, fullname, phone, password, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)


        if extra_fields.get("is_admin") is not True:
            raise ValueError("Superuser must have is_admin=True.")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        

        user = self.create_user(
            email=email,
            fullname=fullname,
            phone=phone,
            password=password,
            **extra_fields,
        )
        user.save(using=self._db)
        return user



def UserImagePath(instance, filename):
    user_slug = str(instance.slug)
    return f"users/{user_slug}/{filename}"


class User(AbstractBaseUser, PermissionsMixin):

    GENDER_CHOICES = [
        ( 'Female', 'Female', ),
        ( 'Male', 'Male', ),
    ]

    ROLE_CHOICES = [
        ( 'admin', 'Admin', ),
        ( 'client', 'Client', ),
        ( 'manager', 'Manager', ),
        ( 'merchant', 'Merchant', ),
    ]

    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True, null=True)

    fullname = models.CharField(max_length=255, verbose_name=_("user name"))
    email = models.EmailField(unique=True, verbose_name=_("email address"))
    phone = models.CharField(max_length=30, verbose_name=_("phone number"))
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True, blank=True)

    gender = models.CharField(max_length=15, choices=GENDER_CHOICES, null=True, blank=True)
    profile_image = models.ImageField(upload_to=UserImagePath, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'fullname', 'phone'
    ]


    def save(self, *args, **kwargs):

        if not self.slug:
            base_slug = slugify(f"{self.fullname}")
            unique_suffix = uuid.uuid4().hex[:10]
            self.slug = f"{base_slug}-{unique_suffix}"

        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.fullname} {self.email}"

