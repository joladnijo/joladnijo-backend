# Generated by Django 3.2 on 2022-03-12 16:53

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AidCenter',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('note', models.TextField(blank=True, max_length=255)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('photo', models.FileField(blank=True, max_length=255, upload_to='aidcenter-photos')),
                ('country_code', models.CharField(max_length=5)),
                ('postal_code', models.CharField(max_length=10)),
                ('city', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=255)),
                ('geo_location', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('call_required', models.CharField(blank=True, choices=[('required', 'required'), ('suggested', 'suggested'), ('denied', 'denied')], max_length=20, null=True)),
                ('money_accepted', models.BooleanField(blank=True, null=True)),
                ('money_description', models.TextField(blank=True, max_length=1023)),
                ('campaign_ending_on', models.DateField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('note', models.TextField(blank=True, max_length=255)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('note', models.TextField(blank=True, max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('facebook', models.URLField(blank=True, max_length=255)),
                ('url', models.URLField(blank=True, max_length=255)),
                ('aid_center', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='joladnijo.aidcenter')),
                ('organization', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='joladnijo.organization')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='aidcenter',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='joladnijo.organization'),
        ),
    ]
