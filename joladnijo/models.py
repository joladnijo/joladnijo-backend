import uuid

from django.contrib.gis.db import models as gis_models
from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class NoteableModel(models.Model):
    note = models.CharField(max_length=255, blank=True)

    class Meta:
        abstract = True


class Organization(BaseModel, NoteableModel):
    name = models.CharField(max_length=255, blank=False, unique=True)
    slug = models.SlugField(max_length=255, blank=False, unique=True)

    def __str__(self) -> str:
        return self.name


class AidCenter(BaseModel, NoteableModel):
    name = models.CharField(max_length=255, blank=False, unique=True)
    slug = models.SlugField(max_length=255, blank=False, unique=True)
    photo = models.FileField(max_length=255, blank=True, upload_to='aidcenter-photos')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    country_code = models.CharField(max_length=5, blank=False)
    postal_code = models.CharField(max_length=10, blank=False)
    city = models.CharField(max_length=50, blank=False)
    address = models.CharField(max_length=255, blank=False)
    geo_location = gis_models.PointField(blank=True, null=True)
    call_required = models.CharField(
        max_length=20, blank=True, null=True,
        choices=(
            ('required', 'required'),
            ('suggested', 'suggested'),
            ('denied', 'denied'),
        ),
    )
    money_accepted = models.BooleanField(blank=True, null=True)
    money_description = models.CharField(max_length=1023, blank=True)
    campaign_ending_on = models.DateField(blank=True, null=True)

    def __str__(self) -> str:
        return '%s - %s (%s)' % (self.organization.name, self.name, self.city)


class Contact(BaseModel, NoteableModel):
    name = models.CharField(max_length=255, blank=False)
    email = models.EmailField(max_length=255, blank=False)
    phone = models.CharField(max_length=20, blank=True)
    facebook = models.URLField(max_length=255, blank=True)
    url = models.URLField(max_length=255, blank=True)
    organization = models.OneToOneField(Organization, on_delete=models.CASCADE, blank=True, null=True)
    aid_center = models.OneToOneField(AidCenter, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self) -> str:
        if self.phone == '':
            return '%s (%s)' % (self.name, self.email)
        return '%s (%s, %s)' % (self.name, self.phone, self.email)

