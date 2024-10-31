import re

from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework.serializers import ModelSerializer, ValidationError

from apps.user_api.constants import (
    PHONE_NUMBER_VALIDATION_REGEX_VALUE,
    PHONE_NUMBER_VALIDATION_ERROR_MESSAGE,
)
from apps.user_api.models import User


class UserSerializer(ModelSerializer):

    class Meta:
        fields = '__all__'
        model = User
        username_validator = UnicodeUsernameValidator()  # this is what Django default user model uses
        phone_number_validation_regex = re.compile(PHONE_NUMBER_VALIDATION_REGEX_VALUE)

    def validate_username(self, data):
        self.Meta.username_validator.__call__(data)
        # if not (data % 20 == 0 and data % 100 == 0):
        #     raise ValidationError(
        #         f'invalid amount {data}; '
        #         'amount must be in steps of 20 and also in cents (e.g. divisible by 100 and 20)'
        #     )
        return data

    def validate_phone_number(self, data):
        # TODO: this is an oversimplified validation just for a starter;
        # As per the case this should implement an appropriate validation or a general one as f.e.
        # https://django-phonenumber-field.readthedocs.io/en/latest/ which is is a port of Google’s libphonenumber
        if not re.match(self.Meta.phone_number_validation_regex, data):
            raise ValidationError(PHONE_NUMBER_VALIDATION_ERROR_MESSAGE)
        return data
