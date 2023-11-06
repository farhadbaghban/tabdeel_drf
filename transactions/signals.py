from django.db.models.signals import post_save
from .models import Transaction, Customer
from conf import logger


def create_a_customer(sender, instance: Transaction, *args, **kwargs):
    if instance.is_raise:
        return

    def raise_amount(exist):
        exist.amount += instance.amount
        exist.save()
        logger.logger.info("logged")

    try:
        exist = Customer.objects.select_for_update().get(
            phone_number=instance.to_number
        )
        raise_amount(exist)
    except Customer.DoesNotExist:
        new = Customer.objects.create(
            phone_number=instance.to_number, amount=instance.amount
        )
        transaction = Transaction.objects.select_for_update().get(pk=instance.id)
        transaction.to_whom = new
        transaction.save()


post_save.connect(create_a_customer, sender=Transaction)
