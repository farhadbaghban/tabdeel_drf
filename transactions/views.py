from django.shortcuts import get_list_or_404
from django.db import transaction
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accounts.models import User
from .models import Transaction, TransactionRaise, Customer
from .serializers import TransactionRaiseSerializers, TransactionSellSerializers


class TransactionRaiseView(APIView):
    serializer_class = TransactionRaiseSerializers
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, *args, **kwargs):
        transactions = get_list_or_404(TransactionRaise, user=request.user)
        ser_data = self.serializer_class(instance=transactions, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        ser_data = self.serializer_class(data=request.POST)
        if ser_data.is_valid():
            valid_data = ser_data.validated_data
            try:
                with transaction.atomic():
                    transactionraise = Transaction.objects.create(
                        is_raise=valid_data["is_raise"],
                        amount=valid_data["amount"],
                        user=user,
                        to_number=None,
                    )
                    user = User.objects.select_for_update().get(pk=user.id)
                    user.credit += transactionraise.amount
                    user.save()
                    ser_data = self.serializer_class(instance=transactionraise)
                    return Response(ser_data.data, status=status.HTTP_201_CREATED)
            except ValidationError as ex:
                return Response(ex.error_dict, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionSellView(APIView):
    serializer_class = TransactionSellSerializers
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, *args, **kwargs):
        transactions = get_list_or_404(Transaction, user=request.user)
        ser_data = self.serializer_class(instance=transactions, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        ser_data = self.serializer_class(data=request.POST)
        if ser_data.is_valid():
            try:
                with transaction.atomic():
                    valid_data = ser_data.validated_data
                    transactionsell = Transaction.objects.create(
                        amount=valid_data["amount"],
                        user=user,
                        to_number=valid_data["to_number"],
                    )
                    seller = User.objects.select_for_update().get(pk=user.id)
                    seller.credit -= valid_data["amount"]
                    seller.save()
                    ser_data = self.serializer_class(instance=transactionsell)
                    return Response(ser_data.data, status=status.HTTP_201_CREATED)
            except ValidationError as ex:
                return Response(ex.error_dict, status=status.HTTP_400_BAD_REQUEST)
        else:
            print(ser_data.errors)
            return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
