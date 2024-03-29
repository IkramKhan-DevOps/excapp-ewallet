import os
from pathlib import Path
import environ

""" __ BASE CONFIGURATIONS __"""
env = environ.Env(
    DEBUG=(bool, False)
)
MAINTENANCE = False
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

""" CONFIGURATIONS -----------------------------------------------------------------------------------------------"""

BASE_URL = env('BASE_URL')
DEBUG = bool(env('DEBUG'))
SECRET_KEY = env('SECRET_KEY')
ENVIRONMENT = env('ENVIRONMENT')
SITE_ID = int(env('SITE_ID'))
DOMAIN_URL = BASE_URL
ALLOWED_HOSTS = [env('ALLOWED_HOST')]

AUTH_USER_MODEL = 'accounts.User'
ROOT_URLCONF = 'cocognite.urls'
WSGI_APPLICATION = 'cocognite.wsgi.application'
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

STRIPE_PUBLISHABLE_KEY = env('STRIPE_PUBLISHABLE_KEY')
STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY')
STRIPE_ENDPOINT_SECRET = env('STRIPE_ENDPOINT_SECRET')
STRIPE_CONNECT_CLIENT_ID = env('STRIPE_CONNECT_CLIENT_ID')
GOOGLE_CALLBACK_ADDRESS = env('GOOGLE_CALLBACK_ADDRESS')

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
LOGIN_REDIRECT_URL = '/accounts/cross-auth/'

""" INSTALLATIONS ------------------------------------------------------------------------------------------------"""

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # REQUIRED_APPLICATIONS
    'crispy_forms',
    'crispy_bootstrap5',
    'ckeditor',
    'qrcode',
    'phonenumber_field',

    # TEMP
    'django_seed',
    'django_filters',

    'rest_framework',
    'rest_framework.authtoken',

    'dj_rest_auth',
    'dj_rest_auth.registration',

    # AUTH_API
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    # SESSION_APP
    'preventconcurrentlogins',

    # USER_APPLICATIONS
    'src.accounts',
    'src.website',

    'src.portals.customer',
    'src.portals.admins',
    'src.payments',
    'src.api',

    # MUST BE AT THE END
    'notifications'
]

""" SECURITY AND MIDDLEWARES -------------------------------------------------------------------------------------"""

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'preventconcurrentlogins.middleware.PreventConcurrentLoginsMiddleware'
]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
}

REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'src.accounts.serializers.RegisterSerializerRestAPI',
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

""" TEMPLATES AND DATABASES -------------------------------------------------------------------------------------- """
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),

    }
}

""" INTERNATIONALIZATION ----------------------------------------------------------------------------------------- """

LANGUAGE_CODE = 'en-us'
TIME_ZONE = env('TIME_ZONE')
USE_I18N = True
USE_L10N = True
USE_TZ = True

""" PATHS STATIC AND MEDIA --------------------------------------------------------------------------------------- """

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'assets')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

""" EMAIL AND ALL AUTH ------------------------------------------------------------------------------------------- """

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'SkiSipWallet <support@skisipwallet.com>'

SOCIALACCOUNT_PROVIDERS = {
    'google': {'SCOPE': ['profile', 'email', ],
               'AUTH_PARAMS': {'access_type': 'online', }}
}

ACCOUNT_LOGOUT_ON_GET = True
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
OLD_PASSWORD_FIELD_ENABLED = True
LOGOUT_ON_PASSWORD_CHANGE = False
ACCOUNT_EMAIL_VERIFICATION = 'none'

""" RESIZER IMAGE --------------------------------------------------------------------------------"""
DJANGORESIZED_DEFAULT_SIZE = [1920, 1080]
DJANGORESIZED_DEFAULT_QUALITY = 75
DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_FORCE_FORMAT = 'JPEG'
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {
    'JPEG': ".jpg",
    'PNG': ".png",
    'GIF': ".gif"
}
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = True

""" DEBUGGING TOOLS """

if ENVIRONMENT != 'server':
    INSTALLED_APPS += [
        'django_browser_reload'
    ]
    MIDDLEWARE += [
        'django_browser_reload.middleware.BrowserReloadMiddleware'
    ]

"""
SECRET_KEY=s(l5vi&5nq3619gdskadhgjaksd981234hlaskhjdlasd
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=donald.duck0762@gmail.com
EMAIL_HOST_PASSWORD=jivcvsjgjgkadtnk
TIME_ZONE=Asia/Calcutta
DB_NAME=db
DB_USER=dbuser
DB_PASSWORD=dbuserpassword
DB_PORT=
STRIPE_PUBLISHABLE_KEY=pk_test_51KNUx8GWh1G1v77h4cAKDbEvH3wEbK4yVZfSGKT5f5wgShK8cipV0ctpNrZ2tqt63fsVmJp4sAk6cs8mogGlzHlL00CTKGtGvE
STRIPE_SECRET_KEY=sk_test_51KNUx8GWh1G1v77hDR40VBVDDZTK2pgUZMk0yxDyN4evl4lBg2LyxFyOQCDoLQWhgy1t9bAzcC63c681rUe5mxtv00vHfKyh2r
STRIPE_ENDPOINT_SECRET=whsec_1d8d3fe0a2aa5e4636cd1343c86fdc72d962593725e8d3a4ab8ad122b8522893
STRIPE_CONNECT_CLIENT_ID=ca_LJXOn5lzLW8IVP0ikolZhksjmSCP4HZa
GOOGLE_CALLBACK_ADDRESS=http://127.0.0.1:8000/accounts/google/login/callback/
SITE_ID=
BASE_URL=http://127.0.0.1:8000/
DOMAIN=127.0.0.1:8000

"""

"""
python manage.py makemigrations accounts admins website payments customer
"""
