from rest_framework import serializers

from . import models


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contact
        exclude = ['organization', 'aid_center']


class OrganizationSerializer(serializers.ModelSerializer):
    contact = ContactSerializer()

    class Meta:
        model = models.Organization
        fields = '__all__'


class AssetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AssetCategory
        fields = '__all__'


class AssetRequestSerializer(serializers.ModelSerializer):
    category = AssetCategorySerializer()

    class Meta:
        model = models.AssetRequest
        exclude = ['aid_center']


class AidCenterSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()
    contact = ContactSerializer()
    geo_location = serializers.JSONField()
    assets_requested = AssetRequestSerializer(many=True, read_only=True)
    assets_fulfilled = AssetRequestSerializer(many=True, read_only=True)
    assets_overloaded = AssetRequestSerializer(many=True, read_only=True)

    class Meta:
        model = models.AidCenter
        fields = '__all__'
