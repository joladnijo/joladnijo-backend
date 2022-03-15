import re
import uuid
from itertools import tee

from django.contrib.gis.db import models as gis_models
from django.db import models
from djangorestframework_camel_case.util import camelize_re, underscore_to_camel
from simple_history.models import HistoricalRecords


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True


class NoteableModel(models.Model):
    note = models.TextField(max_length=255, blank=True)

    class Meta:
        abstract = True


class Organization(BaseModel, NoteableModel):
    name = models.CharField(max_length=255, blank=False, unique=True)
    slug = models.SlugField(max_length=255, blank=False, unique=True)

    def __str__(self) -> str:
        return self.name


def _iterable_pair(i):
    a, b = tee(i)
    next(b, None)
    return zip(a, b)


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
        max_length=20,
        blank=True,
        null=True,
        choices=(
            ('required', 'required'),
            ('suggested', 'suggested'),
            ('denied', 'denied'),
        ),
    )
    money_accepted = models.BooleanField(blank=True, null=True)
    money_description = models.TextField(max_length=1023, blank=True)
    campaign_ending_on = models.DateField(blank=True, null=True)

    def assets_requested(self):
        return self.assetrequest_set.requested()

    def assets_fulfilled(self):
        return self.assetrequest_set.fulfilled()

    def assets_overloaded(self):
        return self.assetrequest_set.overloaded()

    def _changes_of(self, history, obj):
        changes = []
        name = 'this'
        if obj is not None:
            name += '.%s[%s]' % obj
        first = True
        for pair in _iterable_pair(history.order_by('history_date').iterator()):
            old, new = pair
            if first:
                changes.append(
                    {
                        'created': name,
                        'date_time': new.history_date,
                    }
                )
                first = False
            delta = new.diff_against(old)
            for change in delta.changes:
                field = change.field
                if '_' in field:
                    field = re.sub(camelize_re, underscore_to_camel, field)
                changes.append(
                    {
                        'changed': '%s.%s' % (name, field),
                        'from': change.old,
                        'to': change.new,
                        'date_time': new.history_date,
                    }
                )
        return changes

    def feed(self):
        # TODO: ezt talán jó lenne valahogy gyorsítótárazni
        # TODO: mi kell pontosan a feedbe: elég self és assetrequest?
        changes = self._changes_of(self.history.all(), None)
        for request in self.assetrequest_set.all():
            changes += self._changes_of(request.history.all(), ('assetrequest', request.id))
        changes += self._changes_of(self.organization.history.all(), ('organization', self.organization.id))
        if hasattr(self, 'contact'):
            changes += self._changes_of(self.contact.history.all(), ('contact', self.contact.id))
        changes.sort(key=lambda c: c['date_time'], reverse=True)
        return changes

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

    '''
    def clean(self):
        if self.organization is not None and self.aid_center is not None:
            # TODO: itt legyen exception?
    '''


class AssetCategory(BaseModel):
    name = models.CharField(max_length=255, blank=False, unique=True)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL)
    icon = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name_plural = 'Asset categories'

    def __str__(self) -> str:
        if self.parent is not None:
            return '%s (%s)' % (self.name, self.parent.name)
        return self.name

    def clean(self):
        if self.parent == self:
            raise RecursionError("An asset category can't be its own parent")


class AssetRequestManager(models.Manager):
    def requested(self):
        return self.filter(status=AssetRequest.STATUS_REQUESTED)

    def fulfilled(self):
        return self.filter(status=AssetRequest.STATUS_FULFILLED)

    def overloaded(self):
        return self.filter(status=AssetRequest.STATUS_OVERLOADED)


class AssetRequest(BaseModel, NoteableModel):
    STATUS_REQUESTED = 'requested'
    STATUS_FULFILLED = 'fulfilled'
    STATUS_OVERLOADED = 'overloaded'

    objects = AssetRequestManager()

    name = models.CharField(max_length=255, blank=False)
    category = models.ForeignKey(AssetCategory, on_delete=models.CASCADE)
    icon = models.CharField(max_length=50, blank=True)
    aid_center = models.ForeignKey(AidCenter, on_delete=models.CASCADE, blank=False)
    is_urgent = models.BooleanField()
    status = models.CharField(
        max_length=20,
        blank=False,
        default=STATUS_REQUESTED,
        choices=(
            (STATUS_REQUESTED, 'requested'),
            (STATUS_FULFILLED, 'fulfilled'),
            (STATUS_OVERLOADED, 'overloaded'),
        ),
    )

    def __str__(self) -> str:
        return self.name
