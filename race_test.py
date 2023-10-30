import requests
from decimal import Decimal
from concurrent.futures import ThreadPoolExecutor
from subprocess import call
from random import randint


class ConcurrentTest:
    PASSWORD = "123456"

    def __init__(self):
        self.session = requests.Session()
        self.test_raise_result = []
        self.test_sell_result = []
        self.register_url = "http://localhost:8000/accounts/users/register/"
        self.login_url = "http://localhost:8000/accounts/users/login/"
        self.logout_url = "http://localhost:8000/accounts/users/logout/"
        self.check_credit_url = "http://localhost:8000/accounts/users/"
        self.raise_credit_url = "http://localhost:8000/transactions/raise/credit"
        self.sell_url = "http://localhost:8000/transactions/sell/"

    def register(self):
        register_data = {
            "full_name": "farhad test",
            "phone_number": "09397330682",
            "email": "baghbanfarhad@gmail.com",
            "id_card_number": "2050086733",
            "password": self.PASSWORD,
        }
        response = self.session.post(self.register_url, data=register_data)
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
        print(res.text)
        if res.status_code == 201:
            res = res.json()
            res = {"date": res["date"], "amount": res["amount"]}
            self.test_raise_result.append(res)

    def sell_amount_to_number(self, sell_amount, to_number):
        sell_data = {"amount": Decimal(sell_amount), "to_number": to_number}
        res = self.session.post(self.sell_url, data=sell_data)
        print(res.text)
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


class ImplementationDataGenerator:
    def __init__(self, phone_numbers_count, credit_raises_count, sell_amounts_count):
        self.phone_numbers_count = phone_numbers_count
        self.credit_raises_count = credit_raises_count
        self.sell_amounts_count = sell_amounts_count
        self.phone_numbers = []
        self.credit_raises = []
        self.sell_amounts = []

    def create_phone_numbers(self, iteration):
        for i in range(iteration):
            phone_number = str(22222111110 + i)
            self.phone_numbers.append({"phone_number": phone_number})

    def create_raise_credit_amounts(self, iteration):
        for i in range(iteration):
            amount = 200 + i
            self.credit_raises.append({"amount": amount})

    def create_sell_credit_amounts(self, iteration):
        for i in range(iteration):
            amount = 100 + i
            self.sell_amounts.append({"amount": amount})

    def generate(self):
        self.create_phone_numbers(self.phone_numbers_count)
        self.create_raise_credit_amounts(self.credit_raises_count)
        self.create_sell_credit_amounts(self.sell_amounts_count)


call(["python", "manage.py", "flush", "--noinput"])


impdata = ImplementationDataGenerator(40, 40, 40)
impdata.generate()
contest = ConcurrentTest()
contest.register()
contest.login_user()
for i in range(40):
    if randint(1, 13) % 2 == 0:
        contest.raise_credit(impdata.credit_raises[i]["amount"])
    else:
        contest.sell_amount_to_number(
            impdata.sell_amounts[i]["amount"], impdata.phone_numbers[i]["phone_number"]
        )


def equal_test_result():
    equl_positive = Decimal(0)
    equl_mines = Decimal(0)
    for test in contest.test_raise_result:
        equl_positive += Decimal(test["amount"])
        print(f"equl_positive  :  {equl_positive}")
    for test in contest.test_sell_result:
        equl_mines += Decimal(test["amount"])
        print(f"equl_mines  :  {equl_mines}")
    print("------------\n")
    print("len raise (geting from db )")
    print(contest.check_len_raise_transactions())
    print("\n-------------\n")
    print("------------\n")
    print("len raise (geting from success status code  )")
    print(len(contest.test_raise_result))
    print("\n-------------\n")
    print("------------\n")
    print("len sell geting from db ")
    print(contest.check_len_sell_transaction())
    print("\n-------------\n")
    print("------------\n")
    print("len sell (geting from success status code) ")
    print(len(contest.test_sell_result))
    print("\n-------------\n")
    result = equl_positive - equl_mines
    print(result)


def run_tests():
    with ThreadPoolExecutor(10) as exe:
        exe.submit(
            equal_test_result,
        )
        exe.shutdown()


run_tests()
