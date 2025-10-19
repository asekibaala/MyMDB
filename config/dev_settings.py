from config.common_settings import *
DEBUG = True
SECRET_KEY = 'django-insecure-dev-key'
INSTALLED_APPS += [
    'debug_toolbar',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mymdb',
        'USER': 'mymdb',
        'PASSWORD': 'development',
        'HOST': '127.0.0.1',
        'PORT': '5432',

    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'default-localmemcache',
        'TIMEOUT': 5,
    }
}   

#file upload settings
MEDIA_ROOT = os.path.join(BASE_DIR, '../media_root')

# Debug toolbar settings
INTERNAL_IPS = [
    '127.0.0.1',    
]