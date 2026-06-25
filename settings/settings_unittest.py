from .settings import *

LOGGING['loggers']['django']['handlers'] = ['console']
LOGGING['loggers']['settings']['handlers'] = ['console']
LOGGING['loggers']['mis_template']['handlers'] = ['console']
LOGGING['loggers']['cloud_provider']['handlers'] = ['console']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

TESTING_MODE = True
EMAIL_NOTIFICATIONS = False
APP_NOTIFICATION_HOST = ''
DJANGO_ENV = 'UNIT TEST'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES']: (
    'rest_framework.authentication.BasicAuthentication',
)

VISA_USER_POD_NAMESPACE = 'visa-pods-prod'
VISA_DEFAULT_IMAGE_PULL_POLICY = 'IfNotPresent'
VISA_DEFAULT_DNS_POLICY = "ClusterFirst"
VISA_DEFAULT_DEPLOYMENT_PREFIX = f"visa-{DJANGO_ENV.lower()}-user-pod"
VISA_IMAGE_PULL_SECRET_NAME = None
VISA_IMAGE_PULL_SECRET_NAMESPACE = None
VISA_TOTAL_MAX_INSTANCES = 200
VISA_TOTAL_MAX_CPU_AVAILABLE = 100
VISA_TOTAL_MAX_RAM_AVAILABLE = 2000000