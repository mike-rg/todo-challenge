import logging
from functools import wraps

from celery.exceptions import CeleryError

logger = logging.getLogger(__name__)


def handler_celery_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except CeleryError:
            logger.error('Celery is not available.', exc_info=True)

    return wrapper
