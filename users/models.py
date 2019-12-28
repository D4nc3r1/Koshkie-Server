#  Copyright (c) Code Written and Tested by Ahmed Emad in 28/12/2019, 22:43
import os
import uuid

from django.contrib.auth.models import User
from django.db import models


def photo_upload(instance, filename):
    """Gives a unique name to the saved file in models.
    Arguments:
        instance: the file itself, it is not used in this
                  function but it's required by django.
        filename: the name of the file sent by user, it's
                  used here to get the format of the file.

    Returns:
        a unique random name to be saved in the DB.
    """

    return 'users/{0}.{1}'.format(uuid.uuid4().hex, os.path.splitext(filename))


class UserProfileModel(models.Model):
    """The Model of the User Profile."""

    account = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_photo = models.ImageField(upload_to=photo_upload, null=True)
    phone_number = models.BigIntegerField(null=True)
    favourite_products = models.ManyToManyField(to='shops.ProductModel')

    def __str__(self):
        return self.account.username


class UserAddressModel(models.Model):
    """The Model of the User's address."""

    user = models.ForeignKey(to=UserProfileModel, related_name="addresses", on_delete=models.CASCADE)
    sort = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    type = models.CharField(max_length=15)  # house , office or apartment
    street = models.CharField(max_length=255)
    building = models.CharField(max_length=255)
    floor = models.PositiveIntegerField(default=1)
    apartment_no = models.PositiveIntegerField(default=1)
    special_notes = models.TextField(blank=True)
    location_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    location_latitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ("user", "sort")
        ordering = ['sort']
