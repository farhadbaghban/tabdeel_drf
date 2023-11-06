from .models import Customer
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


def check_customer(phone_number):
    try:
        customer = Customer.objects.get(phone_number=phone_number)
        if customer:
            return customer
    except MultipleObjectsReturned:
        return None
    except ObjectDoesNotExist:
        return None
