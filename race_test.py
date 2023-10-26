import json
from decimal import Decimal
import requests
from concurrent.futures import ThreadPoolExecutor
from subprocess import call

# from transactions.models import Transaction


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
        # register_data = {
        #     "full_name": self.user["full_name"],
        #     "phone_number": self.user["phone_number"],
        #     "email": self.user["email"],
        #     "id_card_number": self.user["id_card_number"],
        #     "password": self.user["password"],
        # }
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

    def check_credit_user(self):
        response = self.session.get(f"{self.check_credit_url}{self.user_info['id']}/")
        return response.json()["credit"]


class ImplementationDataGenerator:
    def __init__(self, phone_numbers_count, credit_raises_count, sell_amounts_count):
        # self.users_count = users_count
        self.phone_numbers_count = phone_numbers_count
        self.credit_raises_count = credit_raises_count
        self.sell_amounts_count = sell_amounts_count

        # self.users = []
        self.phone_numbers = []
        self.credit_raises = []
        self.sell_amounts = []

    # def create_users(self, iteration):
    #     for i in range(iteration):
    #         full_name = "farhadtest test" + str(i * ("a"))
    #         email = "test" + str(i * ("a")) + "@email.com"
    #         phone_number = str(22221111110 + i)
    #         id_card_number = str(3333444440 + i)
    #         password = str(123456 + i)
    #         self.users.append(
    #             {
    #                 "full_name": full_name,
    #                 "email": email,
    #                 "phone_number": phone_number,
    #                 "id_card_number": id_card_number,
    #                 "password": password,
    #             }
    #         )

    def create_phone_numbers(self, iteration):
        for i in range(iteration):
            phone_number = str(22222111110 + i)
            self.phone_numbers.append({"phone_number": phone_number})

    def create_raise_credit_amounts(self, iteration):
        for i in range(iteration):
            amount = 1000 + i
            self.credit_raises.append({"amount": amount})

    def create_sell_credit_amounts(self, iteration):
        for i in range(iteration):
            amount = 100 + i
            self.sell_amounts.append({"amount": amount})

    def generate(self):
        # self.create_users(self.users_count)
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
    contest.raise_credit(impdata.credit_raises[i]["amount"])
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
    return equl_positive - equl_mines


print(contest.check_credit_user())
print(equal_test_result())


# test_transactions = Transaction.objects.all()
# print(len(test_transactions))
# def run_tests():
#     with ThreadPoolExecutor(10) as exe:
#         exe.submit(
#             run_single_test,
#         )
#         exe.shutdown()
