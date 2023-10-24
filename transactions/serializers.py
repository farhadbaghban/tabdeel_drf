from rest_framework import serializers


class TransactionRaiseSerializers(serializers.Serializer):
    is_raise = serializers.BooleanField()
    amount = serializers.DecimalField(max_digits=8, decimal_places=2)


class TransactionSellSerializers(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=8, decimal_places=2)
    to_number = serializers.CharField()
