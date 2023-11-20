from decimal import Decimal
from concurrent.futures import ThreadPoolExecutor
from subprocess import call
from random import randint
import threading

# import conf.logger
import concurrent_test
import implementation_data_generator

call(["python", "manage.py", "flush", "--noinput"])


contest = concurrent_test.ConcurrentTest()
contest.register()
contest.login_user()
impdata = implementation_data_generator.ImplementationDataGenerator(10, 10, 10)
impdata.generate()


def equal_test_result():
    for i in range(10):
        contest.raise_credit(impdata.credit_raises[i]["amount"])
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

    def print_some():
        print(
            f"\n ---------\n len raise (from db)\n {contest.check_len_raise_transactions()}\n len raise success status\n{len(contest.test_raise_result)} \n id is {id(threading.current_thread())}\n-----------\n{result}\n"
        )
        print(
            f"\n ---------\n len sell (from db)\n {contest.check_len_sell_transaction()}\n len sell success status\n{len(contest.test_sell_result)} \n id is {id(threading.current_thread())}\n-----------\n{result}\n"
        )

    print_some()


def run_tests(iteration):
    equal_test_result()


def use_multiple_workers():
    print("in use multiple workers")
    with ThreadPoolExecutor(max_workers=300) as executor:
        # different thread ids will get dumped
        futures = [executor.submit(lambda: run_tests(i)) for i in range(50)]
        for future in futures:
            try:
                future.result()
            except Exception:
                pass


if __name__ == "__main__":
    use_multiple_workers()
