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
        fields = ['name', 'icon']
        read_only_fields = ['name', 'icon']


class AssetTypeSerializer(serializers.ModelSerializer):
    category = AssetCategorySerializer()
    icon = serializers.CharField()

    class Meta:
        model = models.AssetType
        fields = '__all__'
        read_only_fields = ['name', 'icon', 'category']


class AssetRequestSerializer(serializers.ModelSerializer):
    type = AssetTypeSerializer()

    class Meta:
        model = models.AssetRequest
        exclude = ['aid_center']

    def build_standard_field(self, field_name, model_field):
        field_class, field_kwargs = super(AssetRequestSerializer, self).build_standard_field(field_name, model_field)
        if field_name == 'status':
            field_kwargs['required'] = True
        return field_class, field_kwargs


class FeedItemSerializer(serializers.ModelSerializer):
    aid_center_name = serializers.CharField(source='aid_center.name')

    class Meta:
        model = models.FeedItem
        exclude = ['user']


class AidCenterSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()
    contact = ContactSerializer()
    geo_location = serializers.JSONField()
    assets_requested = AssetRequestSerializer(many=True, read_only=True)
    assets_urgent = AssetRequestSerializer(many=True, read_only=True)
    assets_fulfilled = AssetRequestSerializer(many=True, read_only=True)
    feed = FeedItemSerializer(many=True, read_only=True)

    class Meta:
        model = models.AidCenter
        fields = '__all__'
