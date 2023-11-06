from decimal import Decimal
from django.db import models
from accounts.models import User
from django.core.validators import DecimalValidator, RegexValidator
from .managers import TransactionManager, TransactionRaiseManager


class Customer(models.Model):
    phone_number = models.CharField(
        max_length=11,
        default="00000000000",
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[0-9]{11}$",
                message="only number are allowed",
                code="invalid phone_number",
            )
        ],
    )
    amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        default=Decimal(0.00),
        validators=[DecimalValidator],
    )


class Transaction(models.Model):
    is_raise = models.BooleanField(default=False, blank=True)
    amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        default=Decimal(0.00),
        validators=[DecimalValidator],
    )
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="utransactions"
    )
    to_whom = models.ForeignKey(
        Customer,
        on_delete=models.DO_NOTHING,
        related_name="ctransaction",
        blank=True,
        null=True,
    )
    to_number = models.CharField(
        max_length=11,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r"^[0-9]{11}$",
                message="only numbers are allowed",
                code="invalid phone_number",
            )
        ],
    )
    date = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    objects = TransactionManager()

    def __str__(self):
        if self.is_raise:
            return f"{self.user} raised {self.amount} credit to his account"
        return f"{self.user} send {self.amount} to {self.to_number}"


class TransactionRaise(Transaction):
    objects = TransactionRaiseManager()

    class Meta:
        proxy = True
