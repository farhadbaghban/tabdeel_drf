from datetime import datetime
from django.contrib.auth.models import BaseUserManager
from django.db.models.query import QuerySet
from .validators import Validate


class UserManager(BaseUserManager):
    def create_user(
        self, full_name, email, phone_number, id_card_number, credit, password
    ):
        if not email:
            raise ValueError("user must have email")
        if not phone_number:
            raise ValueError("user must have phone_number")
        if not full_name:
            raise ValueError("user must have full_name")
        if not id_card_number:
            raise ValueError("user must have id card number!")
        user = self.model(
            full_name=Validate.full_name(full_name),
            email=Validate.email(email),
            phone_number=Validate.phone_number(phone_number),
            id_card_number=Validate.id_card_number(id_card_number),
            credit=Validate.credit(credit),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, full_name, email, phone_number, id_card_number, credit, password
    ):
        user = self.create_user(
            full_name, email, phone_number, id_card_number, credit, password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

    def get_queryset(self):
        QuerySet.filter(is_active=True)
        return super().get_queryset()

    def delete(self):
        self.update(is_active=False, de_activate_date=datetime.date)
        return super().delete()


class DeletedUserManager(BaseUserManager):
    def get_queryset(self):
        QuerySet.filter(is_active=False)
        return super().get_queryset()
