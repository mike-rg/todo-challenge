import os

if os.environ.get('DJANGO_ENV') == 'prod':
    from .prod import *
elif os.environ.get('DJANGO_ENV') == 'local':
    from .local import *
else:
    raise Exception('DJANGO_ENV not set')
