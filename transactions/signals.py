from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import Transaction, Customer
from accounts.models import User


@receiver(post_save, sender=Transaction)
def create_a_customer(sender, instance: Transaction, *args, **kwargs):
    if instance.is_raise:
        return

    if instance.to_whom:
        customer = Customer.objects.select_for_update().get(instance.to_whom.pk)
        customer.amount += instance.amount
        customer.save()
    else:
        Customer.objects.create(phone_number=instance.to_number, amount=instance.amount)
    seller = User.objects.select_for_update().get(pk=instance.user.pk)
    seller.credit -= instance.amount
    seller.save()
