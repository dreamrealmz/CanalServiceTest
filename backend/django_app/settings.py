from .django_settings import *

INSTALLED_APPS += [
    'rest_framework',
    'drf_yasg',
    'solo',
    'google_sheet',
]

# redis conf
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_DB = os.getenv('REDIS_DB')

# logging
LOGS_PATH = os.path.join(BASE_DIR, 'logs/')
if not os.path.isdir(LOGS_PATH):
    os.makedirs(LOGS_PATH)

LOGGING_LEVEL = 'DEBUG' if DEBUG else 'INFO'

LOG_FORMATTING = 'detail' if DEBUG else 'simple'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detail': {
            'format': '%(levelname)s | %(asctime)s | %(module)s | line %(lineno)s | %(message)s'
        },
        'simple': {
            'format': '%(levelname)s | %(asctime)s | %(message)s'
        },
    },
    'handlers': {
        'error': {
                    'level': LOGGING_LEVEL,
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': os.path.join(LOGS_PATH, 'error.log'),
                    'formatter': LOG_FORMATTING,
                    'maxBytes': 2e+7,
                    'backupCount': 10,
                },

    },
    'loggers': {
        'error': {
            'handlers': [
                'error',
            ],
            'level': LOGGING_LEVEL,
            'propagate': False
        },

    },
}

# celery configuration
CELERY_BROKER_URL = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/1'
CELERY_RESULT_BACKEND = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/2'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ENABLE_UTC = False
# CELERYD_CONCURRENCY = os.getenv('CELERYD_CONCURRENCY')
DJANGO_CELERY_BEAT_TZ_AWARE = False

CELERY_BEAT_SCHEDULE = {
    # это задание (get_currency_value) я запускаю каждые 60 секунд, т.к. не знаю, когда будет запущен сервис
    # в теории его должен дергать кронтаб раз в день
    'get_currency_value': {
        'task': 'google_sheet.tasks.get_currency_value.get_currency_value',
        'schedule': 60,
    },
    'parse_google': {
        'task': 'google_sheet.tasks.parse_google.parse_google',
        'schedule': 60,
    },
    'update_database': {
        'task': 'google_sheet.tasks.update_database.update_database',
        'schedule': 60,
    },
    'notify_orders': {
        'task': 'google_sheet.tasks.notify_orders.notify_orders',
        'schedule': 60,
    },
}
