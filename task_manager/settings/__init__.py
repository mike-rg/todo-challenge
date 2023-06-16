import os

from dotenv import load_dotenv

load_dotenv()

if os.getenv('DJANGO_ENV') == 'prod':
    from .prod import *
elif os.getenv('DJANGO_ENV') == 'local':
    from .local import *
elif os.getenv('DJANGO_ENV') == 'test':
    from .test import *
else:
    raise Exception('DJANGO_ENV not set')
