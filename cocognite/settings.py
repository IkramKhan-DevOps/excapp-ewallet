import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

""" CONFIGURATIONS -----------------------------------------------------------------------------------------------"""

AUTH_USER_MODEL = 'accounts.User'
ROOT_URLCONF = 'cocognite.urls'
WSGI_APPLICATION = 'cocognite.wsgi.application'
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

SECRET_KEY = 's(l5vi&5nq3619gdskadhgjaksd981234hlaskhjdlasd'

DEBUG = True
SERVER = True
ALLOWED_HOSTS = ['*']

if SERVER:
    STRIPE_PUBLISHABLE_KEY = 'pk_test_51KOk8vBXdgScJTxkzqhOkxuFkEQMmPEovaPOPkasrJSfFQytvh0gXHcZop8eB7KZzr0YWpWK2pr3vHAZMDoMpRsc00czwWEk29'
    STRIPE_SECRET_KEY = 'sk_test_51KOk8vBXdgScJTxk22T3bOcTpYhOu508E6udhxCMrezc7AM3DCqtGfvMESsPuQ0pHokZj4zmZx45esCbDdxpUaS3005oAq8vyq'
    GOOGLE_CALLBACK_ADDRESS = "https://exarthdev4.pythonanywhere.com/accounts/google/login/callback/"
    SITE_ID = 2
    DOMAIN_URL = 'https://exarthdev4.pythonanywhere.com/'
else:
    STRIPE_PUBLISHABLE_KEY = 'pk_test_51KOk8vBXdgScJTxkzqhOkxuFkEQMmPEovaPOPkasrJSfFQytvh0gXHcZop8eB7KZzr0YWpWK2pr3vHAZMDoMpRsc00czwWEk29'
    STRIPE_SECRET_KEY = 'sk_test_51KOk8vBXdgScJTxk22T3bOcTpYhOu508E6udhxCMrezc7AM3DCqtGfvMESsPuQ0pHokZj4zmZx45esCbDdxpUaS3005oAq8vyq'
    GOOGLE_CALLBACK_ADDRESS = "http://127.0.0.1:8000/accounts/google/login/callback/"
    SITE_ID = 1
    DOMAIN_URL = 'http://127.0.0.1:8000/'


CRISPY_TEMPLATE_PACK = 'bootstrap4'
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
    'ckeditor',

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
TIME_ZONE = 'Asia/Calcutta'
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
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'donald.duck0762@gmail.com'
EMAIL_HOST_PASSWORD = 'jivcvsjgjgkadtnk'
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
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

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
