import re

from django.core.exceptions import ValidationError


def validate_telephone_number(number):
    pattern = r'^\+\d{11}$'
    if not bool(re.match(pattern, number)):
        raise ValidationError(
            'Телефонный номер должен начинаться с +, содержать 11 цифр'
        )


def numeric_only(operatore_code):
    if operatore_code.isdigit() is False:
        raise ValidationError('Код оператора должен содержать только цифры')
