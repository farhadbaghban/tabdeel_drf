from django.db.models.signals import pre_save
from .models import Transaction, Customer


def create_a_customer(sender, instance: Transaction, *args, **kwargs):
    if instance.is_raise:
        return

    if instance.to_whom:
        customer = Customer.objects.select_for_update().get(instance.to_whom.pk)
        customer.amount += instance.amount
        customer.save()
    else:
        customer = Customer.objects.create(
            phone_number=instance.to_number, amount=instance.amount
        )
        instance.to_whom = customer


pre_save.connect(create_a_customer, sender=Transaction)
