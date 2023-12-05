import os
from decimal import Decimal
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from subprocess import call
from random import randint
import threading
import time
import multiprocessing

# import conf.logger
import concurrent_test
import implementation_data_generator

call(["python", "manage.py", "flush", "--noinput"])


class RunTest:
    def __init__(self):
        self.test_impdata = []

    def get_input(self):
        self.users_num = int(input("\n please enter number of users :  "))
        self.customer_num = int(input("\n please enter number of cutomers :  "))
        self.raise_num = int(input("\n please enter number of raises :  "))

    def create_impdata(self):
        for _ in range(self.users_num):
            _impdata = implementation_data_generator.ImplementationDataGenerator(
                self.customer_num, self.raise_num, self.customer_num
            )
            _impdata.generate()
            self.test_impdata.append(_impdata)

    def runnig_test(self, impdata):
        register_data = impdata.register_data
        session = impdata.username_session[0]
        username = register_data["full_name"]
        print(register_data)
        print(session)
        print(username)
        session = session[username]
        print(register_data)
        print(session)
        contest = concurrent_test.ConcurrentTest(register_data, session)
        contest.register()
        contest.login_user()
        for i in range(self.raise_num):
            contest.raise_credit(impdata.credit_raises[i]["amount"])
        for i in range(self.customer_num):
            contest.sell_amount_to_number(
                impdata.sell_amounts[i]["amount"],
                impdata.phone_numbers[i]["phone_number"],
            )
        equl_positive = Decimal(0)
        equl_mines = Decimal(0)
        for test in contest.test_raise_result:
            equl_positive += Decimal(test["amount"])
        for test in contest.test_sell_result:
            equl_mines += Decimal(test["amount"])
        result = equl_positive - equl_mines
        print(
            f"\n ---------\n len raise (from db)\n {contest.check_len_raise_transactions()}\n len raise success status\n{len(contest.test_raise_result)} \n id is {id(threading.current_thread())}\n-----------\n{result}\n"
        )
        print(
            f"\n ---------\n len sell (from db)\n {contest.check_len_sell_transaction()}\n len sell success status\n{len(contest.test_sell_result)} \n id is {id(threading.current_thread())}\n-----------\n{result}\n"
        )


def use_multiple_threads():
    start = time.perf_counter()
    test = RunTest()
    test.get_input()
    test.create_impdata()
    with ThreadPoolExecutor(max_workers=300) as executor:
        # executor.map(run_tests, tries)
        futures = [
            executor.submit(test.runnig_test, impdata) for impdata in test.test_impdata
        ]
        try:
            for future in futures:
                print(future.result())
        except ValueError as e:
            print(e)
    end = time.perf_counter()
    print(f"It took {end - start} seconds to finish")


def use_multiple_process():
    start = time.perf_counter()
    test = RunTest()
    test.get_input()
    test.create_impdata()
    with ProcessPoolExecutor(
        max_workers=multiprocessing.cpu_count() * 2 + 1
    ) as executor:
        # executor.map(run_tests, tries)
        futures = [
            executor.submit(test.runnig_test, impdata) for impdata in test.test_impdata
        ]
        try:
            for future in futures:
                print(future.result())
        except ValueError as e:
            print(e)
    end = time.perf_counter()
    print(f"It took {end - start} seconds to finish")


if __name__ == "__main__":
    value = input("Please Enter : \n 1 : Multiple Thread \n 2: Multiple Process\n    ")
    if int(value) == 1:
        use_multiple_threads()
    elif int(value) == 2:
        use_multiple_process()
