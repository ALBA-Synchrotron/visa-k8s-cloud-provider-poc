from .settings import *

ALLOWED_HOSTS = ['*']

LOGGING['loggers']['django']['handlers'] = ['console']
LOGGING['loggers']['settings']['handlers'] = ['console']
LOGGING['loggers']['mis_template']['handlers'] = ['console']
LOGGING['loggers']['cloud_provider']['handlers'] = ['console']

DJANGO_ENV = 'LOCAL'

APP_HOST = 'http://localhost:8000'
APP_NOTIFICATION_HOST = 'http://localhost:8000'

EMAIL_HOST = ''
EMAIL_PORT = '1025'
EMAIL_HOST_USER = None
EMAIL_HOST_PASSWORD = None
EMAIL_USE_TLS = False
VISA_PUBLIC_KEY_NAME = 'test-pam-key'
VISA_USER_POD_NAMESPACE = 'visa-pods-test'
VISA_DEFAULT_IMAGE_PULL_POLICY = 'Always'
VISA_DEFAULT_DNS_POLICY = "ClusterFirst"
VISA_DEFAULT_DEPLOYMENT_PREFIX = f"visa-{DJANGO_ENV.lower()}-user-instance"
VISA_IMAGE_PULL_SECRET_NAME = None
VISA_IMAGE_PULL_SECRET_NAMESPACE = None
