from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 's447i&4(zdwn8!2z=evo%ke%1jbp2u6bq3zk(c&z0p$2x6pzmp'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

ADMIN=[('Admin','Admin@blossoms.in'),('S_Dev','jokesprogramming@gmail.com')]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'django.contrib.postgres',
    'HOME.apps.HomeConfig',
    'PRODUCTR.apps.ProductrConfig',
    
    

    
  
]

#SOCIAL_AUTH_POSTGRES_JSONFIELD = True
MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'social_django.middleware.SocialAuthExceptionMiddleware',
    

]



ROOT_URLCONF = 'djangoProject1.urls'
TEMPLATE = os.path.join(BASE_DIR, "templates")
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE],

        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
               # 'social_django.context_processors.backends',

            ],
        },
    },
]

WSGI_APPLICATION = 'djangoProject1.wsgi.application'


# LOGIN_URL='user_login'
# SIGNUP_URL='user_signup'
# LOGIN_REQUIRED_URL='dashboard'



# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {

    'default': {
        
        'ENGINE': 'django.db.backends.postgresql_psycopg2',

        'NAME': 'Sai',

        'USER': 'postgres',

        'PASSWORD': 'programming_jokes.py.3',

        'HOST': 'localhost',

        'PORT':5432,
        
        #  'ENGINE': 'django.db.backends.sqlite3',
        #  'NAME': 'blossom4.sqlite3',
    }
}






# LOGIN_URL = 'user_login'
# LOGOUT_URL = 'user_logout'
# LOGIN_REDIRECT_URL = 'dashboard'
# SOCIAL_AUTH_URL_NAMESPACE = 'social'

# SOCIAL_AUTH_FACEBOOK_KEY='794252641215280'
# SOCIAL_AUTH_FACEBOOK_SECRET='ede098b7128d9b5ae830658245b8a823'

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
     os.path.join(BASE_DIR, 'static'),
 ]
STATIC_ROOT=os.path.join(BASE_DIR,'sta')
MEDIA_URL='/media/'
MEDIA_ROOT=os.path.join(BASE_DIR,'media')


##SMPT
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST ='smtp.gmail.com'
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER='foundationssaksham@gmail.com'
EMAIL_HOST_PASSWORD='mogwdgnsdctqhgkw'
DEFAULT_FROM_EMAIL='Bloosms<noreply@sakshamfoundations.in>'


#
#