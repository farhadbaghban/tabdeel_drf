from rest_framework import serializers
from .models import Transaction, TransactionRaise


class TransactionRaiseSerializers(serializers.ModelSerializer):
    class Meta:
        model = TransactionRaise
        exclude = ["to_whom", "to_number", "deleted"]
        extra_kwargs = {"user": {"read_only": True}, "date": {"read_only": True}}

    is_raise = serializers.BooleanField()
    amount = serializers.DecimalField(max_digits=8, decimal_places=2)


class TransactionSellSerializers(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        exclude = ["to_whom", "deleted"]
        read_only_fields = ["user", "date"]

    amount = serializers.DecimalField(max_digits=8, decimal_places=2)
    to_number = serializers.CharField()
