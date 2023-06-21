import os

from .base import *

DEBUG = True

# Email settings
if os.getenv('EMAIL_BACKEND') == 'File':
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = '/tmp/app-messages'
else:
    EMAIL_HOST = os.getenv('EMAIL_HOST')
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
    EMAIL_PORT = os.getenv('EMAIL_PORT')


# Email verification
REGISTRATION_EMAIL_CONFIRM_ENABLED = True
REGISTRATION_EMAIL_CONFIRM_MODEL_FIELD = "email_verified"
REGISTRATION_EMAIL_BASE_URL = "http://localhost:8000"
REGISTRATION_EMAIL_FROM = "noreply@example.org"


# Logging settings
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': '/var/logs/app.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'apps': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}
