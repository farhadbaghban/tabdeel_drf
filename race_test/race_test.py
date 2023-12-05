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


def print_some():
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


def run_tests(iteration):
    print(
        f"start process with  {os.getpid()} \n and thread with {threading.get_ident()}"
    )
    equal_test_result()


def use_multiple_threads():
    start = time.perf_counter()
    print("in use multiple Threads\n")
    tries = [i for i in range(50)]
    with ThreadPoolExecutor(max_workers=300) as executor:
        # executor.map(run_tests, tries)
        futures = [executor.submit(run_tests, i) for i in range(10)]
        try:
            for future in futures:
                print(future.result())
        except ValueError as e:
            print(e)
    print_some()
    end = time.perf_counter()
    print(f"It took {end - start} seconds to finish")


def use_multiple_process():
    start = time.perf_counter()
    print("in use multiple Process")
    # tries = [i for i in range(50)]
    with ProcessPoolExecutor(
        max_workers=multiprocessing.cpu_count() * 2 + 1
    ) as executor:
        # executor.map(run_tests, tries)
        futures = [executor.submit(run_tests, i) for i in range(10)]
        try:
            for future in futures:
                print(future.result())
        except ValueError as e:
            print(e)
    print_some()
    end = time.perf_counter()
    print(f"It took {end - start} seconds to finish")


if __name__ == "__main__":
    value = input("Please Enter : \n 1 : Multiple Thread \n 2: Multiple Process\n    ")
    if int(value) == 1:
        use_multiple_threads()
    elif int(value) == 2:
        use_multiple_process()
