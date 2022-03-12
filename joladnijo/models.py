import uuid

from django.contrib.gis.db import models as gis_models
from django.db import models
from itertools import tee

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


def pair_iterable_for_delta_changes(iterable):
    a, b = tee(iterable)
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
        max_length=20, blank=True, null=True,
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

    def _changes_of(self, history, field = 'self', id = None):
        changes = []
        field_prefix = None
        if field != 'self':
            field_prefix = field
            if id is not None:
                field_prefix += '.%s' % id
        for record_pair in pair_iterable_for_delta_changes(history.order_by('history_date').iterator()):
            old_record, new_record = record_pair
            delta = new_record.diff_against(old_record)
            for change in delta.changes:
                changes.append({
                    # TODO: legyen külön mezőben a field és id, vagy jó így?
                    'changed': change.field if field_prefix is None else '%s.%s' % (field_prefix, change.field),
                    'from': change.old,
                    'to': change.new,
                    'date_time': new_record.history_date,
                })
        return changes

    def feed(self):
        # TODO: ezt talán jó lenne valahogy gyorsítótárazni
        # TODO: mi kell pontosan a feedbe: elég self és assetrequest?
        changes = self._changes_of(self.history.all())
        for request in self.assetrequest_set.all():
            changes += self._changes_of(request.history.all(), 'assetrequest', request.id)
        changes += self._changes_of(self.organization.history.all(), 'organization')
        if self.contact is not None:
            changes += self._changes_of(self.contact.history.all(), 'contact')
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


class AssetCategory(BaseModel):
    name = models.CharField(max_length=255, blank=False, unique=True)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL)
    icon = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name_plural = 'Asset categories'

    def __str__(self) -> str:
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
        max_length=20, blank=False, default=STATUS_REQUESTED,
        choices=(
            (STATUS_REQUESTED, 'requested'),
            (STATUS_FULFILLED, 'fulfilled'),
            (STATUS_OVERLOADED, 'overloaded'),
        ),
    )

    def __str__(self) -> str:
        return self.name
