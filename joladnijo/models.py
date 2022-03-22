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
    name = models.CharField(verbose_name='Név', max_length=255, blank=False, unique=True)
    slug = models.SlugField(max_length=255, blank=False, unique=True)
    history = HistoricalRecords()

    class Meta(BaseModel.Meta, NoteableModel.Meta):
        verbose_name = 'Szervezet'
        verbose_name_plural = 'Szervezetek'

    def __str__(self) -> str:
        return self.name


class AidCenter(BaseModel, NoteableModel):
    name = models.CharField(verbose_name='Név', max_length=255, blank=False, unique=True)
    slug = models.SlugField(max_length=255, blank=False, unique=True)
    photo = models.FileField(verbose_name='Kép', max_length=255, blank=True, upload_to='aidcenter-photos')
    organization = models.ForeignKey(Organization, verbose_name='Szervezet', on_delete=models.CASCADE)
    country_code = models.CharField(verbose_name='Ország', max_length=5, blank=False)
    postal_code = models.CharField(verbose_name='Irányítószám', max_length=10, blank=False)
    city = models.CharField(verbose_name='Település', max_length=50, blank=False)
    address = models.CharField(verbose_name='Cím', max_length=255, blank=False)
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

    def assets_fulfilled(self):
        return self.assetrequest_set.fulfilled()

    def assets_overloaded(self):
        return self.assetrequest_set.overloaded()

    def feed(self):
        return self.feeditem_set.all()

    def __str__(self) -> str:
        return '%s - %s (%s)' % (self.organization.name, self.name, self.city)


class Contact(BaseModel, NoteableModel):
    name = models.CharField(verbose_name='Név', max_length=255, blank=False)
    email = models.EmailField(verbose_name='E-mail cím', max_length=255, blank=False)
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
    name = models.CharField(verbose_name='Név', max_length=255, blank=False, unique=True)
    icon = models.CharField(verbose_name='Ikon', max_length=50, blank=True)
    category = models.ForeignKey('self', verbose_name='Kategória', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Kategória'
        verbose_name_plural = 'Kategóriák'

    def __str__(self) -> str:
        return self.name


class AssetType(AssetCategory):
    class Meta:
        proxy = True
        verbose_name = 'Típus'
        verbose_name_plural = 'Típusok'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__class__ = AssetType

    def __str__(self) -> str:
        if self.category is not None:
            return '%s (%s)' % (self.name, self.category.name)
        return self.name


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

    name = models.CharField(verbose_name='Név', max_length=255, blank=False)
    type = models.ForeignKey(AssetType, verbose_name='Típus', blank=True, null=True, on_delete=models.SET_NULL)
    aid_center = models.ForeignKey(AidCenter, verbose_name='Gyűjtőhely', blank=False, on_delete=models.CASCADE)
    is_urgent = models.BooleanField(verbose_name='Sürgős')
    status = models.CharField(
        verbose_name='Státusz',
        max_length=20,
        blank=False,
        default=STATUS_REQUESTED,
        choices=(
            (STATUS_REQUESTED, 'szükség van rá'),
            (STATUS_FULFILLED, 'van elég'),
            (STATUS_OVERLOADED, 'túl sok van'),
        ),
    )
    history = HistoricalRecords()

    class Meta(BaseModel.Meta, NoteableModel.Meta):
        verbose_name = 'Adomány'
        verbose_name_plural = 'Adományok'

    def __str__(self) -> str:
        return self.name


class FeedItem(BaseModel, NoteableModel):
    name = models.CharField(verbose_name='Név', max_length=255, blank=False)
    icon = models.CharField(verbose_name='Ikon', max_length=50, blank=True)
    timestamp = models.DateTimeField(verbose_name='Időpont', auto_now_add=True)
    asset_request = models.ForeignKey(
        AssetRequest, verbose_name='Adomány', blank=True, null=True, on_delete=models.SET_NULL
    )
    aid_center = models.ForeignKey(AidCenter, verbose_name='Gyűjtőhely', blank=False, on_delete=models.CASCADE)
    status_old = models.CharField(verbose_name='Korábbi állapot', max_length=255, blank=True)
    status_new = models.CharField(verbose_name='Új állapot', max_length=255, blank=True)

    class Meta(BaseModel.Meta, NoteableModel.Meta):
        verbose_name = 'Változás'
        verbose_name_plural = 'Változások'
        ordering = ['-timestamp']
