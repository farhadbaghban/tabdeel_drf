from django.urls import path
from .views import TransactionRaiseView, TransactionSellView

app_name = "transactions"
urlpatterns = [
    path("raise/credit", TransactionRaiseView.as_view(), name="raise_credit"),
    path("sell/", TransactionSellView.as_view(), name="sell"),
]
