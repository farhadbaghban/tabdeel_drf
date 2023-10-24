import requests
from concurrent.futures import ThreadPoolExecutor


username = ""
password = ""

session = requests.Session()


def register():
    session.post()


def login():
    session.post()


def run_single_test():
    session.post()


def run_tests():
    with ThreadPoolExecutor(10) as exe:
        exe.submit(
            run_single_test,
        )
        exe.shutdown()


register()
login()
run_tests()
