from decimal import Decimal
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import RegexValidator, MinValueValidator
from .managers import UserManager, DeletedUserManager


class User(AbstractBaseUser):
    full_name = models.CharField(
        max_length=100,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"(^[A-Za-z]{3,16})([ ]{0,1})([A-Za-z]{3,45})?([ ]{0,1})?([A-Za-z]{3,25})?([ ]{0,1})?([A-Za-z]{3,15})",
                message="only characters are allowed ",
                code="invalid full_name",
            )
        ],
    )
    email = models.EmailField(max_length=100, unique=True, blank=False)
    phone_number = models.CharField(
        max_length=11,
        unique=True,
        blank=False,
        validators=[
            RegexValidator(
                regex=r"^[0-9]{11}$",
                message="only number are allowed",
                code="invalid phone_number",
            )
        ],
    )
    id_card_number = models.CharField(
        max_length=10,
        unique=True,
        blank=False,
        validators=[
            RegexValidator(
                regex=r"^[0-9]{10}?",
                message="only number are allowed",
                code="invalid id_card_number",
            )
        ],
    )
    credit = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal("0.00"),
        blank=True,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    de_activate_date = models.DateTimeField(blank=True, null=True)
    registered_date = models.DateTimeField(auto_now_add=True)
    objects = UserManager()
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["full_name", "email", "id_card_number"]

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
