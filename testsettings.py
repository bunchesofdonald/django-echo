DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'echo',
)

SECRET_KEY = 'abcde12345'

USE_TZ = True

ROOT_URLCONF = 'echo.urls'
MIDDLEWARE_CLASSES = ()
