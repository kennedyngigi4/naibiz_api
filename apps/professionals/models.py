import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from apps.accounts.models import User
# Create your models here.



class Profession(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("profession category"))
    price = models.PositiveIntegerField(verbose_name=_("listing price"))
    active_days = models.PositiveIntegerField(verbose_name=_("active days"))
    is_free = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(verbose_name=_("description"))
    icon = models.TextField(null=True)

    def __str__(self):
        return self.name


class Specialization(models.Model):
    profession = models.ForeignKey(Profession, on_delete=models.CASCADE, related_name='specializations')
    name = models.CharField(max_length=255)

    class Meta:
        unique_together = ( 'profession', 'name')
        verbose_name = 'Specialization'
        verbose_name_plural = 'Specializations'

    def __str__(self):
        return f"{self.profession.name} - {self.name}"
    


def professionalImagePath(instance, filename):
    user_id = str(instance.user.id).replace("-","")
    return f"professionals/{user_id}/{filename}"


class ProfessionalProfile(models.Model):

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    slug = models.SlugField(unique=True, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='professional_profile')
    profession = models.ForeignKey(Profession, on_delete=models.SET_NULL, null=True, blank=True)
    specializations = models.ManyToManyField(Specialization, blank=True)

    fullname = models.CharField(max_length=255, null=True)
    title = models.CharField(max_length=100, help_text="e.g. Dr., Eng., Adv.")
    license_number = models.CharField(max_length=100, blank=True, null=True)
    license_issuer = models.CharField(max_length=255, blank=True, null=True)
    license_issue_date = models.DateField(blank=True, null=True)
    license_expiry_date = models.DateField(blank=True, null=True)
    consultation_fee = models.PositiveIntegerField(blank=True, null=True)

    bio = models.TextField(blank=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(null=True, blank=True)
    website = models.URLField(blank=True)
    location = models.TextField(blank=True, null=True)
    location_latLng = models.CharField(max_length=200, blank=True, null=True)

    profile_image = models.ImageField(upload_to=professionalImagePath, null=True, blank=True)
    banner_image = models.ImageField(upload_to=professionalImagePath, null=True, blank=True)

    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)


    class Meta:
        verbose_name = 'Professional Profile'
        verbose_name_plural = 'Professional Profiles'

    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.fullname}")
            unique_suffix = uuid.uuid4().hex[:8]
            self.slug = f"{base_slug}-{unique_suffix}"
            
        super().save(*args, **kwargs)
       

    def __str__(self):
        return f"{self.title} {self.user.fullname} - {self.profession}"




class Education(models.Model):
    professional = models.ForeignKey(ProfessionalProfile, on_delete=models.CASCADE, related_name='education')
    institution = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    field_of_study = models.CharField(max_length=255)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.degree} at {self.institution}"



class WorkExperience(models.Model):
    professional = models.ForeignKey(ProfessionalProfile, on_delete=models.CASCADE, related_name='work_experience')
    position = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.position} at {self.company}"



