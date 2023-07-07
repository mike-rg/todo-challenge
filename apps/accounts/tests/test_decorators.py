from unittest.mock import patch

from celery.exceptions import CeleryError

from apps.accounts.decorators import handler_celery_exceptions


@handler_celery_exceptions
def dummy_function():
    raise CeleryError('Celery is not available.')


def test_handler_celery_exceptions():
    with patch('apps.accounts.decorators.logger') as mocked_logger:
        dummy_function()
    mocked_logger.error.assert_called_once_with('Celery is not available.', exc_info=True)
