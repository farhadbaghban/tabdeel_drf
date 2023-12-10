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
        session = session[username]
        contest = concurrent_test.ConcurrentTest(register_data, session)
        contest.register()
        contest.login_user()
        with open(
            f"./race_test/statuscodes/raise_status.txt",
            mode="a",
        ) as a:
            for i in range(self.raise_num):
                contest.raise_credit(impdata.credit_raises[i]["amount"])
                a.write(
                    f"raise_status is : {str(contest.status_raise)} from {username} at this process : {os.getpid()} and this thread : {threading.get_ident()}  records in db {contest.check_len_raise_transactions()} and user credit is {contest.check_credit_user()}\n"
                )
        with open(
            f"./race_test/statuscodes/cell_status.txt",
            mode="a",
        ) as a:
            for i in range(self.customer_num):
                contest.sell_amount_to_number(
                    impdata.sell_amounts[i]["amount"],
                    impdata.phone_numbers[i]["phone_number"],
                )

                a.write(
                    f"cell_status is : {str(contest.status_raise)} from {username} at this process : {os.getpid()} and this thread : {threading.get_ident()}  records in db {contest.check_len_sell_transaction()} and user credit is {contest.check_credit_user()}\n"
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
    end = time.perf_counter()
    print(f"\nIt took {end - start} seconds to finish\n")
    call(["python", "./race_test/test_result.py"])


def use_multiple_process():
    start = time.perf_counter()
    test = RunTest()
    test.get_input()
    test.create_impdata()
    with ProcessPoolExecutor(max_workers=50) as executor:
        # executor.map(run_tests, tries)
        # max_workers=multiprocessing.cpu_count() * 2 + 1
        futures = [
            executor.submit(test.runnig_test, impdata) for impdata in test.test_impdata
        ]
        try:
            for future in futures:
                print(future.result())
        except ValueError as e:
            print(e)
    end = time.perf_counter()
    print(f"\nIt took {end - start} seconds to finish\n")
    call(["python", "./race_test/test_result.py"])


if __name__ == "__main__":
    value = input("Please Enter : \n 1 : Multiple Thread \n 2: Multiple Process\n    ")
    if int(value) == 1:
        use_multiple_threads()
    elif int(value) == 2:
        use_multiple_process()
