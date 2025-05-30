# Generated by Django 4.2 on 2025-05-12 13:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('primary_phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='Enter phone number with country code', max_length=128, null=True, region=None)),
                ('primary_postcode', models.CharField(blank=True, max_length=24, null=True)),
                ('primary_zipcode', models.CharField(blank=True, max_length=24, null=True)),
                ('primary_address', models.TextField(blank=True, max_length=255, null=True)),
                ('primary_city', models.CharField(blank=True, max_length=100, null=True)),
                ('primary_county', models.CharField(blank=True, max_length=100, null=True)),
                ('primary_country', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Account Profile',
                'verbose_name_plural': 'Account Profiles',
                'ordering': ['-created_at'],
            },
        ),
    ]
