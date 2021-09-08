from django.contrib.auth import password_validation


def validate_password(value):
    """
    validate password
    """
    password_validation.validate_password(value)
