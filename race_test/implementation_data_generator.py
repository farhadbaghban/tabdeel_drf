import random
import string
import requests


class ImplementationDataGenerator:
    PASSWORD = "123456"

    def __init__(self, phone_numbers_count, credit_raises_count, sell_amounts_count):
        self.phone_numbers_count = phone_numbers_count
        self.credit_raises_count = credit_raises_count
        self.sell_amounts_count = sell_amounts_count
        self.phone_numbers = []
        self.credit_raises = []
        self.sell_amounts = []
        self.register_data = {}
        self.username_session = []

    def create_user_info(self):
        self.full_name = "user" + "".join(
            random.choice(string.ascii_lowercase + string.ascii_uppercase)
            for _ in range(10)
        )
        self.register_data = {
            "full_name": self.full_name,
            "phone_number": "".join(random.choice(string.digits) for _ in range(11)),
            "email": "user"
            + "".join(
                random.choice(string.ascii_lowercase + string.ascii_uppercase)
                for _ in range(10)
            )
            + "@email.com",
            "id_card_number": "".join(random.choice(string.digits) for _ in range(10)),
            "password": self.PASSWORD,
        }

    def create_user_session(self):
        self.username_session.append({self.full_name: requests.Session()})

    def create_phone_numbers(self, iteration):
        for i in range(iteration):
            _phone_number = str(22222111110 + i)
            self.phone_numbers.append({"phone_number": _phone_number})

    def create_raise_credit_amounts(self, iteration):
        for i in range(iteration):
            _amount = 200 + i
            self.credit_raises.append({"amount": _amount})

    def create_sell_credit_amounts(self, iteration):
        for i in range(iteration):
            _amount = 100 + i
            self.sell_amounts.append({"amount": _amount})

    def generate(self):
        self.create_user_info()
        self.create_user_session()
        self.create_phone_numbers(self.phone_numbers_count)
        self.create_raise_credit_amounts(self.credit_raises_count)
        self.create_sell_credit_amounts(self.sell_amounts_count)
