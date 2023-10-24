from django.test import SimpleTestCase
from django.urls import reverse, resolve
from transactions.views import *


class TestUrls(SimpleTestCase):
    def test_raise_credit_resolve(self):
        url = reverse("transactions:raise_credit")
        self.assertEquals(resolve(url).func.view_class, TransactionRaiseView)

    def test_sell_resolves(self):
        url = reverse("transactions:sell")
        self.assertEquals(resolve(url).func.view_class, TransactionSellView)
