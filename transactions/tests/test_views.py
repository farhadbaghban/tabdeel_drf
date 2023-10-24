import json
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from decimal import Decimal
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from accounts.models import User
from transactions.models import TransactionRaise, Transaction, Customer


class RaiseViewTest(APITestCase):
    def setUp(self):
        PASSWORD = "123456"
        self.user = User.objects.create_user(
            full_name="farhad baghbannn",
            email="baghbannnfarhad@email.com",
            phone_number="09397300002",
            id_card_number="2050080003",
            password=PASSWORD,
        )
        self.client = APIClient()
        self.client.login(phone_number=self.user.phone_number, password=PASSWORD)
        return super().setUp()

    def test_get_raise_transactions(self):
        url = reverse("transactions:raise_credit")
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
        TransactionRaise.objects.create(
            is_raise=True,
            amount=Decimal("100.00"),
            user=self.user,
            to_whom=None,
            to_number="09119490000",
        )
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data[0]["is_raise"], True)
        self.assertEquals(len(response.data), 1)

    def test_post_raise_transaction(self):
        url = reverse("transactions:raise_credit")
        transaction_raise = {"is_raise": "True", "amount": "100.00"}
        response = self.client.post(url, transaction_raise)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)


class SellerViewTest(APITestCase):
    def setUp(self):
        PASSWORD = "123456"
        self.user = User.objects.create_user(
            full_name="farhad baghbannn",
            email="baghbannnfarhad@email.com",
            phone_number="09397300002",
            id_card_number="2050080003",
            password=PASSWORD,
        )
        self.user.credit = Decimal("1000")
        self.user.save()
        self.client = APIClient()
        self.client.login(phone_number=self.user.phone_number, password=PASSWORD)
        return super().setUp()

    def test_customer_create(self):
        PHONE_NUMBER = "09111234567"
        url = reverse("transactions:sell")
        transaction_raise = {"amount": "100.00", "to_number": PHONE_NUMBER}
        response = self.client.post(url, transaction_raise)
        Customer.objects.get(phone_number=PHONE_NUMBER)

    def test_customer_not_created(self):
        PHONE_NUMBER = "09111234567"
        url = reverse("transactions:sell")
        transaction_raise = {"amount": "1001.00", "to_number": PHONE_NUMBER}
        response = self.client.post(url, transaction_raise)
        Customer.objects.get(phone_number=PHONE_NUMBER)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)


class TaskTest(APITestCase):
    PASSWORD = "123456"

    def setUp(self):
        self.customers = [(f"0935555555{i}", i + 100) for i in range(10)]
        self.user = User.objects.create_user(
            full_name="farhad baghbann",
            email="baghbannfarhad@email.com",
            phone_number="09397300002",
            id_card_number="2050080003",
            password=self.PASSWORD,
        )
        self.user.credit = Decimal("1000")
        self.user.save()
        self.user2 = User.objects.create_user(
            full_name="farhad baghbannnn",
            email="baghbannnfarhad@email.com",
            phone_number="09390000002",
            id_card_number="2000080003",
            password=self.PASSWORD,
        )
        self.user2.credit = Decimal("1000")
        self.user2.save()
        self.client = APIClient()
        return super().setUp()

    def test_raise_users_credit(self):
        for user in [self.user, self.user2]:
            self.client.login(phone_number=user.phone_number, password=self.PASSWORD)
            url = reverse("transactions:raise_credit")
            transaction_raise = {"is_raise": "True", "amount": "100.00"}
            transaction_raise2 = {"is_raise": "True", "amount": "200.00"}
            self.client.post(url, transaction_raise)
            self.client.post(url, transaction_raise2)
            user = User.objects.get(phone_number=user.phone_number)
            self.assertEquals(user.credit, Decimal("1300.00"))
            sell_url = reverse("transactions:sell")
            for i in self.customers:
                transaction_sell = {"amount": Decimal(i[1]), "to_number": i[0]}
                response = self.client.post(sell_url, transaction_sell)
                self.assertEquals(response.status_code, status.HTTP_201_CREATED)
            user.refresh_from_db()
            self.assertEquals(user.credit, Decimal("255"))
            self.client.logout()
