from typing import Any
from django.core.management.base import BaseCommand, CommandParser
from transactions.models import Transaction
from accounts.models import User


class CommandError:
    def __init__(self, e) -> None:
        self.e = e

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        print(self.e)


class Command(BaseCommand):
    help = "get transaction raised"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("username", type=str)

    def handle(self, *args: Any, **options: Any):
        try:
            user = User.objects.get(full_name=options["username"])
            transactions = Transaction.objects.filter(user=user, is_raise=False)
            return transactions
        except User.DoesNotExist as e:
            raise CommandError(e)
