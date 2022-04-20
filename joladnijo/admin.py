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
    fields = (('name', 'slug'), 'description', 'note')
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
            'Alap infók',
            {
                'fields': (
                    ('name', 'slug'),
                    'photo',
                    'organization',
                    'description',
                ),
            },
        ),
        (
            'Helyszín',
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
            'Egyéb',
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

    @admin.display(description='Szervezet', ordering='name')
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

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return obj is not None and obj.assettype_set.count() == 0


@admin.register(models.AssetType)
class AssetTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_link']
    list_filter = ['category']
    fields = (
        'name',
        'category',
    )

    @admin.display(description='Kategória', ordering='name')
    def category_link(self, obj):
        url = reverse('admin:joladnijo_assetcategory_change', args=[obj.category.pk])
        return mark_safe('<a href="%s">%s</a>' % (url, obj.category))

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return obj is not None and obj.assetrequest_set.count() == 0


@admin.register(models.AssetRequest)
class AssetRequestAdmin(SimpleHistoryAdmin):
    list_display = ['name', 'aid_center_link', 'status']
    list_filter = ['type', 'status', 'aid_center']
    fields = (
        'name',
        'type',
        'aid_center',
        'status',
    )

    @admin.display(description='Gyűjtőhely', ordering='name')
    def aid_center_link(self, obj):
        url = reverse('admin:joladnijo_aidcenter_change', args=[obj.aid_center.pk])
        return mark_safe('<a href="%s">%s</a>' % (url, obj.aid_center))


@admin.register(models.FeedItem)
class FeedItemAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'name', 'asset_request_link', 'aid_center_link', 'status_old', 'status_new']
    list_filter = ['asset_request', 'aid_center', 'user']
    fields = (
        ('name', 'icon'),
        'asset_request',
        'aid_center',
        'status_old',
        'status_new',
        'note',
        'user',
    )
    read_only_fields = ['timestamp']

    @admin.display(description='Adomány', ordering='name')
    def asset_request_link(self, obj):
        url = reverse('admin:joladnijo_assetrequest_change', args=[obj.asset_request.pk])
        return mark_safe('<a href="%s">%s</a>' % (url, obj.asset_request))

    @admin.display(description='Gyűjtőhely', ordering='name')
    def aid_center_link(self, obj):
        url = reverse('admin:joladnijo_aidcenter_change', args=[obj.aid_center.pk])
        return mark_safe('<a href="%s">%s</a>' % (url, obj.aid_center))

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
