from collections.abc import Iterable
from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager, DeletedUserManager
from .validators import Validate


class User(AbstractBaseUser):
    full_name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True, blank=False)
    phone_number = models.CharField(max_length=11, unique=True, blank=False)
    id_card_number = models.CharField(max_length=10, unique=True, blank=False)
    credit = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    de_activate_date = models.DateTimeField(default=None, blank=True, null=True)
    registered_date = models.DateTimeField(auto_now_add=True)
    objects = UserManager()
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["full_name", "email", "phone_number", "id_card_number"]

    class Meta:
        verbose_name = "seller"
        verbose_name_plural = "sellers"
        ordering = ["credit", "full_name"]

    def __str__(self):
        return f"{self.full_name} has {self.credit} credit"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save()
        return super().delete(using, keep_parents)

    def clean(self):
        self.full_name = Validate.full_name(self.full_name)
        self.email = Validate.email(self.email)
        self.phone_number = Validate.phone_number(self.phone_number)
        self.id_card_number = Validate.id_card_number(self.id_card_number)
        self.credit = Validate.credit(self.credit)
        return super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(User, self).save(*args, **kwargs)

    @property
    def is_staff(self):
        return self.is_admin


class DeletedUsers(User):
    objects = DeletedUserManager()

    class Meta:
        proxy = True
