from rest_framework import serializers

from . import models


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Organization
        fields = '__all__'


class AidCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AidCenter
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contact
        fields = '__all__'
