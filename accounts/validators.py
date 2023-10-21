import re
from django.core.exceptions import ValidationError


class Validate:
    def full_name(self, full_name):
        regex = re.compile(r"^[A-Za-z]{3,}\s^[A-Za-z]{3,}?")
        if full_name:
            if re.fullmatch(regex, full_name):
                return full_name
            else:
                raise ValidationError("invalid full name")
        else:
            raise ValueError("you must have full name")

    def email(self, email):
        regex = re.compile(
            r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        )
        if email:
            if re.fullmatch(regex, str(email)):
                return email
            else:
                raise ValidationError("invalid Email")
        else:
            raise ValueError("You must have email")

    def phone_number(self, phone_number):
        regex = re.compile(r"^\\+?[1-9][0-9]{,11}$")
        if phone_number:
            if re.fullmatch(regex, phone_number):
                return phone_number
            else:
                raise ValidationError("invalid phone Number")
        else:
            raise ValueError("you must haves Email")

    def id_card_number(self, id_card_number):
        regex = re.compile(r"^[0-9]{10}?")
        if id_card_number:
            if re.fullmatch(regex, id_card_number):
                return id_card_number
            else:
                raise ValidationError("invalid id card number")
        else:
            raise ValueError("you must haves Email")

    def credit(self, credit):
        regex = re.compile(r"^[0-9]+(\.[0-9]+)?$")
        if credit:
            if re.fullmatch(regex, str(credit)):
                return credit
            else:
                raise ValidationError("invalid credit")
        return "Null"
