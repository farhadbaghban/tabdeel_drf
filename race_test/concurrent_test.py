import requests
from decimal import Decimal


class ConcurrentTest:
    PASSWORD = "123456"

    def __init__(self, register_data, username_session):
        self.session = username_session
        self.register_data = register_data
        self.test_raise_result = []
        self.test_sell_result = []
        self.register_url = "http://localhost:8000/accounts/users/register/"
        self.login_url = "http://localhost:8000/accounts/users/login/"
        self.logout_url = "http://localhost:8000/accounts/users/logout/"
        self.check_credit_url = "http://localhost:8000/accounts/users/"
        self.raise_credit_url = "http://localhost:8000/transactions/raise/credit"
        self.sell_url = "http://localhost:8000/transactions/sell/"

    def register(self):
        response = self.session.post(self.register_url, data=self.register_data)
        self.user_info = response.json()

    def login_user(self):
        login_data = {
            "phone_number": self.user_info["phone_number"],
            "password": self.PASSWORD,
        }
        self.session.post(self.login_url, data=login_data)

    def logout(self):
        self.session.get(self.logout_url)

    def raise_credit(self, raise_amount):
        raise_data = {"is_raise": True, "amount": Decimal(raise_amount)}
        res = self.session.post(self.raise_credit_url, data=raise_data)
        if res.status_code == 201:
            res = res.json()
            res = {"date": res["date"], "amount": res["amount"]}
            self.test_raise_result.append(res)

    def sell_amount_to_number(self, sell_amount, to_number):
        sell_data = {"amount": Decimal(sell_amount), "to_number": to_number}
        res = self.session.post(self.sell_url, data=sell_data)
        if res.status_code == 201:
            res = res.json()
            res = {"date": res["date"], "amount": res["amount"]}
            self.test_sell_result.append(res)

    def check_len_raise_transactions(self):
        res = self.session.get(self.raise_credit_url)
        return len(res.json())

    def check_len_sell_transaction(self):
        res = self.session.get(self.sell_url)
        return len(res.json())

    def check_credit_user(self):
        response = self.session.get(f"{self.check_credit_url}{self.user_info['id']}/")
        return response.json()["credit"]
