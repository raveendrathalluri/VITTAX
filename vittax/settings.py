# vittax/settings.py
from pathlib import Path
import os

import pymysql
pymysql.install_as_MySQLdb()


BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'vittax-secret-key-change-in-production-2024'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'services',
    'contact',
    'admindashboard',
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'vittax.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    # 'DIRS': [BASE_DIR / 'templates'],
    'DIRS': [os.path.join(BASE_DIR, 'templates')], 
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
            'accounts.context_processors.navigation_menu',  

        ],
    },
}]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'vittax',          # Database name
#         'USER': 'vittax_admin',      # Username
#         'PASSWORD': 'aG8dYEif9FW6q7C25zdZ1j6eIZVeLe3e',# Password
#         'HOST': 'postgresql://vittax_admin:aG8dYEif9FW6q7C25zdZ1j6eIZVeLe3e@dpg-d6csad7gi27c7387lb70-a.oregon-postgres.render.com/vittax',        # Host from Render
#         'PORT': '5432',            # Default PostgreSQL port
#     }
# }

# import dj_database_url

# DATABASES = {
#     'default': dj_database_url.parse(
#         "postgresql://vittax_admin:aG8dYEif9FW6q7C25zdZ1j6eIZVeLe3e@dpg-d6csad7gi27c7387lb70-a.oregon-postgres.render.com/vittax"
#     )
# }


AUTH_USER_MODEL = 'accounts.CustomUser'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'


STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Email settings
EMAIL_BACKEND       = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST          = 'smtp.gmail.com'
EMAIL_PORT          = 587
EMAIL_USE_TLS       = True
EMAIL_HOST_USER     = 'nellore.dharani0984@gmail.com'       # ← change
EMAIL_HOST_PASSWORD = 'xnxs guli khpc iaku'    # ← change
DEFAULT_FROM_EMAIL  = 'VITTAX <nellore.dharani0984@gmail.com>'
ADMIN_EMAIL         = 'nellore.dharani0984@gmail.com'       # receives contact alerts

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]
# Source - https://stackoverflow.com/a/20896732
# Posted by pzp, modified by community. See post 'Timeline' for change history
# Retrieved 2026-02-21, License - CC BY-SA 4.0


