from django import forms
from django.contrib import admin
from django.contrib.gis import admin as gis_admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from simple_history.admin import SimpleHistoryAdmin

from . import models


class ContactInline(admin.StackedInline):
    model = models.Contact
    fields = (
        'name',
        'email',
        'phone',
        'facebook',
        'url',
        'note',
    )

    class Meta:
        abstract = True


class OrganizationContactInline(ContactInline):
    fk_name = 'organization'


class AidCenterContactInline(ContactInline):
    fk_name = 'aid_center'


@admin.register(models.Organization)
class OrganizationAdmin(SimpleHistoryAdmin):
    list_display = ['name']
    fields = (('name', 'slug'), 'note')
    prepopulated_fields = {'slug': ['name']}
    inlines = [OrganizationContactInline]


@admin.register(models.AidCenter)
class AidCenterAdmin(gis_admin.GeoModelAdmin, SimpleHistoryAdmin):
    list_display = ['name', 'city', 'organization_link']
    list_filter = ['organization']
    readonly_fields = ['organization_link']
    prepopulated_fields = {'slug': ['name']}
    default_lat = 47.180116
    default_lon = 19.503996
    default_zoom = 7
    fieldsets = (
        (
            'Basic info',
            {
                'fields': (
                    ('name', 'slug'),
                    'photo',
                    'organization',
                ),
            },
        ),
        (
            'Location',
            {
                'fields': (
                    'country_code',
                    ('postal_code', 'city'),
                    'address',
                    'geo_location',
                ),
            },
        ),
        (
            'Other',
            {
                'fields': (
                    'campaign_ending_on',
                    'call_required',
                    'note',
                ),
            },
        ),
    )
    inlines = [AidCenterContactInline]

    @admin.display(
        description='Organization',
        ordering='name',
    )
    def organization_link(self, obj):
        url = reverse('admin:joladnijo_organization_change', args=[obj.organization.pk])
        return mark_safe('<a href="%s">%s</a>' % (url, obj.organization))


@admin.register(models.Contact)
class ContactAdmin(SimpleHistoryAdmin):
    list_display = ['name', 'email', 'phone']
    list_filter = ['organization', 'aid_center']
    fields = (
        'name',
        'email',
        'phone',
        'facebook',
        'url',
        'organization',
        'aid_center',
        'note',
    )


@admin.register(models.AssetCategory)
class AssetCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    fields = (('name', 'icon'),)

    def get_queryset(self, request):
        return super(AssetCategoryAdmin, self).get_queryset(request).filter(category__isnull=True)

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return obj is not None and obj.assetcategory_set.count() == 0


class AssetTypeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].required = True

    class Meta:
        model = models.AssetType
        fields = ['name', 'icon', 'category']


@admin.register(models.AssetType)
class AssetTypeAdmin(admin.ModelAdmin):
    form = AssetTypeForm
    list_display = ['name', 'category']
    list_filter = ['category']
    fields = (
        ('name', 'icon'),
        'category',
    )

    def get_queryset(self, request):
        return super(AssetTypeAdmin, self).get_queryset(request).filter(category__isnull=False)

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return obj is not None and obj.assetrequest_set.count() == 0


@admin.register(models.AssetRequest)
class AssetRequestAdmin(SimpleHistoryAdmin):
    list_display = ['name', 'aid_center_link', 'is_urgent', 'status']
    list_filter = ['type', 'is_urgent', 'status', 'aid_center']
    fields = (
        ('name', 'icon'),
        'type',
        'aid_center',
        ('status', 'is_urgent'),
    )

    @admin.display(
        description='Aid center',
        ordering='name',
    )
    def aid_center_link(self, obj):
        url = reverse('admin:joladnijo_aidcenter_change', args=[obj.aid_center.pk])
        return mark_safe('<a href="%s">%s</a>' % (url, obj.aid_center))
