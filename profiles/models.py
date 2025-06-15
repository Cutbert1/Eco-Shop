from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.


class AccountProfile(models.Model):
    """
    Stores user profile information including contact details and
    shipping information for an authenticated user.

    Each profile linked one-to-one with a User instance.
    Also records timestamps for creation and last updat
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    primary_phone_number = PhoneNumberField(
        null=True, blank=True, help_text="Enter phone number with country code"
        )
    primary_address = models.CharField(max_length=255, null=True, blank=True)
    primary_city = models.CharField(max_length=100, null=True, blank=True)
    primary_county = models.CharField(max_length=100, null=True, blank=True)
    primary_postcode = models.CharField(max_length=24, null=True, blank=True)
    primary_country = CountryField(
        blank_label='Select Country', null=True, blank=True
        )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Account Profile"
        verbose_name_plural = "Account Profiles"
        ordering = ['-created_at']

    def __str__(self):
        return f"Profile for {self.user.username}"


@receiver(post_save, sender=User)
def create_or_update_account_profile(sender, instance, created, **kwargs):
    """
    Signal receiver that ensures each User has an associated AccountProfile
    """
    if created:
        AccountProfile.objects.create(user=instance)
    instance.accountprofile.save()
