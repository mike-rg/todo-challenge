from django.utils import timezone

from .constants import EMAIL_EXPIRATION_DAYS


def get_expiration_date():
    """Returns the expiration date for the verification token.

    Calculates the expiration date by adding the number of days specified in EMAIL_EXPIRATION_DAYS
    to the current date and time.

    Returns:
        datetime: The expiration date for the verification token.

    Arguments:
        None

    """
    return timezone.now() + timezone.timedelta(days=EMAIL_EXPIRATION_DAYS)
