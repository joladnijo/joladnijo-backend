from django.contrib import admin
from django.contrib.gis import admin as gis_admin
from django.utils.safestring import mark_safe
from django.urls import reverse
from . import models


@admin.register(models.Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name']
    fields = (('name', 'slug'), 'note')
    prepopulated_fields = {'slug': ['name']}


@admin.register(models.AidCenter)
class AidCenterAdmin(gis_admin.GeoModelAdmin):
    list_display = ['name', 'city', 'organization_link']
    list_filter = ['organization']
    readonly_fields = ['organization_link']
    prepopulated_fields = {'slug': ['name']}
    default_lat = 47.180116
    default_lon = 19.503996
    default_zoom = 7
    fieldsets = (
        ('Basic info', {
            'fields': (
                ('name', 'slug'),
                'photo',
                'organization',
            ),
        }),
        ('Location', {
            'fields': (
                'country_code',
                ('postal_code', 'city'),
                'address',
                'geo_location',
            ),
        }),
        ('Contact', {
            'fields': ('call_required',),
        }),
        ('Needs', {
            'fields': (
                'money_accepted',
                'money_description',
                'campaign_ending_on',
            ),
        }),
        ('Other', {
            'fields': ('note',),
        }),
    )

    def organization_link(self, obj):
        url = reverse('admin:joladnijo_organization_change', args=[obj.organization.pk])
        return mark_safe('<a href="%s">%s</a>' % (url, obj.organization))
    organization_link.short_description = 'organization'


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
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
