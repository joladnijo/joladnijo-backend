import uuid

from django.contrib.gis.db import models as gis_models
from django.db import models
from simple_history.models import HistoricalRecords


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class NoteableModel(models.Model):
    note = models.TextField(verbose_name='Megjegyzések', max_length=255, blank=True)

    class Meta:
        abstract = True


class Organization(BaseModel, NoteableModel):
    name = models.CharField(verbose_name='Név', max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    history = HistoricalRecords()

    class Meta(BaseModel.Meta, NoteableModel.Meta):
        verbose_name = 'Szervezet'
        verbose_name_plural = 'Szervezetek'

    def __str__(self) -> str:
        return self.name


class AidCenter(BaseModel, NoteableModel):
    name = models.CharField(verbose_name='Név', max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    photo = models.FileField(verbose_name='Kép', max_length=255, blank=True, upload_to='aidcenter-photos')
    organization = models.ForeignKey(Organization, verbose_name='Szervezet', on_delete=models.CASCADE)
    country_code = models.CharField(verbose_name='Ország', max_length=5)
    postal_code = models.CharField(verbose_name='Irányítószám', max_length=10)
    city = models.CharField(verbose_name='Település', max_length=50)
    address = models.CharField(verbose_name='Cím', max_length=255)
    geo_location = gis_models.PointField(verbose_name='Koordináták', blank=True, null=True)
    call_required = models.CharField(
        verbose_name='Hívás szükséges?',
        max_length=20,
        blank=True,
        null=True,
        choices=(
            ('required', 'required'),
            ('suggested', 'suggested'),
            ('denied', 'denied'),
        ),
    )
    campaign_ending_on = models.DateField(verbose_name='Gyűjtés vége', blank=True, null=True)
    history = HistoricalRecords()

    class Meta(BaseModel.Meta, NoteableModel.Meta):
        verbose_name = 'Gyűjtőhely'
        verbose_name_plural = 'Gyűjtőhelyek'

    def assets_requested(self):
        return self.assetrequest_set.requested()

    def assets_urgent(self):
        return self.assetrequest_set.urgent()

    def assets_fulfilled(self):
        return self.assetrequest_set.fulfilled()

    def feed(self):
        return self.feeditem_set.all()

    def __str__(self) -> str:
        return '%s - %s (%s)' % (self.organization.name, self.name, self.city)


class Contact(BaseModel, NoteableModel):
    name = models.CharField(verbose_name='Név', max_length=255)
    email = models.EmailField(verbose_name='E-mail cím', max_length=255)
    phone = models.CharField(verbose_name='Telefonszám', max_length=20, blank=True)
    facebook = models.URLField(verbose_name='Facebook profil', max_length=255, blank=True)
    url = models.URLField(verbose_name='Egyéb url', max_length=255, blank=True)
    organization = models.OneToOneField(
        Organization, verbose_name='Szervezet', blank=True, null=True, on_delete=models.CASCADE
    )
    aid_center = models.OneToOneField(
        AidCenter, verbose_name='Gyűjtőhely', blank=True, null=True, on_delete=models.CASCADE
    )
    history = HistoricalRecords()

    class Meta(BaseModel.Meta, NoteableModel.Meta):
        verbose_name = 'Kapcsolattartó'
        verbose_name_plural = 'Kapcsolattartók'

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
    name = models.CharField(verbose_name='Név', max_length=255, unique=True)
    icon = models.CharField(verbose_name='Ikon', max_length=50, blank=True)

    class Meta:
        verbose_name = 'Kategória'
        verbose_name_plural = 'Kategóriák'

    def __str__(self) -> str:
        return self.name


class AssetType(BaseModel):
    name = models.CharField(verbose_name='Név', max_length=255, unique=True)
    category = models.ForeignKey(AssetCategory, verbose_name='Kategória', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Típus'
        verbose_name_plural = 'Típusok'

    def icon(self):
        return self.category.icon

    def __str__(self) -> str:
        return '%s (%s)' % (self.name, self.category.name)


class AssetRequestManager(models.Manager):
    def requested(self):
        return self.filter(status=AssetRequest.STATUS_REQUESTED)

    def urgent(self):
        return self.filter(status=AssetRequest.STATUS_URGENT)

    def fulfilled(self):
        return self.filter(status=AssetRequest.STATUS_FULFILLED)


class AssetRequest(BaseModel, NoteableModel):
    STATUS_REQUESTED = 'requested'
    STATUS_URGENT = 'urgent'
    STATUS_FULFILLED = 'fulfilled'

    objects = AssetRequestManager()

    name = models.CharField(verbose_name='Név', max_length=255)
    type = models.ForeignKey(AssetType, verbose_name='Típus', on_delete=models.CASCADE)
    aid_center = models.ForeignKey(AidCenter, verbose_name='Gyűjtőhely', on_delete=models.CASCADE)
    status = models.CharField(
        verbose_name='Státusz',
        max_length=20,
        default=STATUS_REQUESTED,
        choices=(
            (STATUS_REQUESTED, 'szükség van rá'),
            (STATUS_URGENT, 'sürgős'),
            (STATUS_FULFILLED, 'van elég'),
        ),
    )
    history = HistoricalRecords()

    class Meta(BaseModel.Meta, NoteableModel.Meta):
        verbose_name = 'Adomány'
        verbose_name_plural = 'Adományok'

    def __str__(self) -> str:
        return self.name


class FeedItem(BaseModel, NoteableModel):
    name = models.CharField(verbose_name='Név', max_length=255)
    icon = models.CharField(verbose_name='Ikon', max_length=50, blank=True)
    timestamp = models.DateTimeField(verbose_name='Időpont', auto_now_add=True)
    asset_request = models.ForeignKey(
        AssetRequest, verbose_name='Adomány', blank=True, null=True, on_delete=models.SET_NULL
    )
    aid_center = models.ForeignKey(AidCenter, verbose_name='Gyűjtőhely', on_delete=models.CASCADE)
    status_old = models.CharField(verbose_name='Korábbi állapot', max_length=255, blank=True, null=True)
    status_new = models.CharField(verbose_name='Új állapot', max_length=255, blank=True, null=True)

    class Meta(BaseModel.Meta, NoteableModel.Meta):
        verbose_name = 'Változás'
        verbose_name_plural = 'Változások'
        ordering = ['-timestamp']
