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


class AidCenterSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()
    contact = ContactSerializer()

    class Meta:
        model = models.AidCenter
        fields = '__all__'
