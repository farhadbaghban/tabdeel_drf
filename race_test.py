import requests
from decimal import Decimal
from concurrent.futures import ThreadPoolExecutor
from subprocess import call
from random import randint
import threading


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
        # print(res.text)
        if res.status_code == 201:
            res = res.json()
            res = {"date": res["date"], "amount": res["amount"]}
            self.test_raise_result.append(res)

    def sell_amount_to_number(self, sell_amount, to_number):
        sell_data = {"amount": Decimal(sell_amount), "to_number": to_number}
        res = self.session.post(self.sell_url, data=sell_data)
        # print(res.text)
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


contest = ConcurrentTest()
contest.register()
contest.login_user()


def equal_test_result():
    impdata = ImplementationDataGenerator(40, 40, 40)
    impdata.generate()
    for i in range(40):
        if randint(1, 3) % 2 == 0:
            contest.raise_credit(impdata.credit_raises[i]["amount"])
        else:
            contest.sell_amount_to_number(
                impdata.sell_amounts[i]["amount"],
                impdata.phone_numbers[i]["phone_number"],
            )
    equl_positive = Decimal(0)
    equl_mines = Decimal(0)
    for test in contest.test_raise_result:
        equl_positive += Decimal(test["amount"])
        # print(f"equl_positive  :  {equl_positive}")
    for test in contest.test_sell_result:
        equl_mines += Decimal(test["amount"])
        # print(f"equl_mines  :  {equl_mines}")
    result = equl_positive - equl_mines

    def print_some():
        print(
            f"\n ---------\n len raise (from db)\n {contest.check_len_raise_transactions()}\n len raise success status\n{len(contest.test_raise_result)} \n id is {id(threading.current_thread())}\n-----------\n{result}\n"
        )
        print(
            f"\n ---------\n len sell (from db)\n {contest.check_len_sell_transaction()}\n len sell success status\n{len(contest.test_sell_result)} \n id is {id(threading.current_thread())}\n-----------\n{result}\n"
        )
        # print("------------\n")
        # print(f"len raise (geting from db ){id(threading.current_thread())}")
        # print(contest.check_len_raise_transactions())
        # print("\n-------------\n")
        # print("------------\n")
        # print(
        #     f"len raise (geting from success status code){id(threading.current_thread())}"
        # )
        # print(len(contest.test_raise_result))
        # print("\n-------------\n")
        # print("------------\n")
        # print(f"len sell geting from db {id(threading.current_thread())}")
        # print(contest.check_len_sell_transaction())
        # print("\n-------------\n")
        # print("------------\n")
        # print(
        #     f"len sell (geting from success status code){id(threading.current_thread())}"
        # )
        # print(len(contest.test_sell_result))
        # print("\n-------------\n")
        # print(result)

    print_some()


# def run_tests():
#     with ThreadPoolExecutor(10) as exe:
#         exe.submit(
#             equal_test_result,
#         )
#         exe.shutdown()


def run_tests(iteration):
    for i in range(iteration):
        equal_test_result()


def use_multiple_workers():
    print("in use multiple workers")
    with ThreadPoolExecutor(max_workers=10) as executor:
        # different thread ids will get dumped
        futures = [executor.submit(lambda: run_tests(i)) for i in range(3)]
        for future in futures:
            try:
                future.result()
            except Exception:
                pass


if __name__ == "__main__":
    use_multiple_workers()
