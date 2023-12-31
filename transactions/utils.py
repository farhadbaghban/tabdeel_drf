from django.db import IntegrityError, transaction
from .models import Transaction, Customer
from conf import logger

"check if customer exist ==> raise amount, else create a new customer"


def add_customer(instance, customer):
    transaction = Transaction.objects.select_for_update().get(pk=instance.id)
    transaction.to_whom = customer
    transaction.save()
    return True


def customer_raise_amount(instance: Transaction, *args, **kwargs):
    try:
        exist = Customer.objects.select_for_update().get(
            phone_number=instance.to_number
        )
        exist.amount += instance.amount
        exist.save()
        if add_customer(instance, exist):
            logger.logger.info("logged")
            return True
        else:
            return False
    except Customer.DoesNotExist:
        try:
            new = Customer.objects.create(
                phone_number=instance.to_number, amount=instance.amount
            )
            if add_customer(instance, new):
                return True
            else:
                return False
        except IntegrityError:
            return False
