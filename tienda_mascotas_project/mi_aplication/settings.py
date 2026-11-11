# tienda_mascotas_project/mi_aplication/settings.py
# ⚠️ IMPORTACIONES Y CARGA DE DOTENV
'''
from dotenv import load_dotenv
import os
from pathlib import Path




BASE_DIR = Path(__file__).resolve().parent.parent

# Esto DEBE ser lo primero que se ejecute para cargar tus credenciales
load_dotenv()



# tienda_mascotas_project/settings.py (Al final)




# Build paths inside the project like this: BASE_DIR / 'subdir'.



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_7i*7yp&slhm-5r$7l-9ksl^@q-lgadtwryul)x(*#xbqz&i9@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# settings.py
CARRITO_SESSION_ID = 'carrito'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
# ... Tus apps existentes
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'catalogo.apps.CatalogoConfig',
    'carrito.apps.CarritoConfig', # Si ya creaste la app carrito
    'ordenes.apps.OrdenesConfig', #para las ordenes
    'widget_tweaks',# <--- ¡Añade esto!

]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

# ⚠️ AÑADE ESTA LÍNEA AQUÍ (es el requisito de allauth)
    'allauth.account.middleware.AccountMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mi_aplication.urls'


# tienda_mascotas_project/mi_aplication/settings.py
# ...

# Configuración de allauth (¡CORREGIDA!)

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_ON_GET = True

# La nueva forma de definir el login:
ACCOUNT_LOGIN_METHODS = ['email', 'username']

# Campos requeridos en el formulario de registro (si quisiéramos añadir más campos):
# Como queremos que el email sea obligatorio, lo gestionamos implícitamente así:
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']
# Esto sigue siendo útil para deshabilitar el campo de username

ACCOUNT_EMAIL_VERIFICATION = 'none' # Recomendado para desarrollo (se puede cambiar a 'mandatory' luego)


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # TU NUEVO PROCESSOR:
                'catalogo.context_processors.processors.categorias_visibles',
                'carrito.context_processors.carrito',
            ],
        },
    },
]

WSGI_APPLICATION = 'mi_aplication.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tienda_mascotas_db',   # nombre de tu base
        'USER': 'postgres',          # usuario de PostgreSQL
        'PASSWORD': '1929', # contraseña del usuario
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_URL = '/static/'

STATICFILES_DIRS = [
BASE_DIR / 'tienda_mascotas_project' / 'static',
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# settings.py (Añadir al final)

# --- CONFIGURACIÓN DE STRIPE ---
# Clave Pública de Prueba (para usar en el frontend)
STRIPE_PUBLISHABLE_KEY = 'pk_test_*********************************'

# Clave Secreta de Prueba (para usar en el servidor/backend)
STRIPE_SECRET_KEY = 'sk_test_*********************************'

# ⚠️ CLAVE SECRETA DEL WEBHOOK (Importante para verificar la autenticidad de la notificación)
STRIPE_WEBHOOK_SECRET = 'whsec_xxxxxxxxxxxxxxxxxxxxxxxxxxx'

STRIPE_PUBLIC_KEY = "tu_clave_publica"

# --- CONFIGURACIÓN DE ARCHIVOS DE MEDIOS (IMÁGENES) ---

# URL de acceso público para los archivos de media (http://127.0.0.1:8000/media/...)
MEDIA_URL = '/media/'




ACCOUNT_FORMS = {
   # 'login': 'mi_aplication.forms.CustomLoginForm',  # RUTA CORREGIDA
    'signup': 'mi_aplication.forms.RegistroForm', # RUTA CORREGIDA
}



'''

# tienda_mascotas_project/mi_aplication/settings.py

# ⚠️ IMPORTACIONES Y CARGA DE DOTENV
from dotenv import load_dotenv
from pathlib import Path


# ✅ BASE_DIR como objeto Path (¡no lo redefinas después!)
BASE_DIR = Path(__file__).resolve().parent.parent

# Esto DEBE ser lo primero que se ejecute para cargar tus credenciales
load_dotenv()

# --- CONFIGURACIÓN GENERAL ---
SECRET_KEY = 'django-insecure-_7i*7yp&slhm-5r$7l-9ksl^@q-lgadtwryul)x(*#xbqz&i9@'
DEBUG = False
ALLOWED_HOSTS = ['*']

# --- CONFIGURACIÓN DE SESIÓN DEL CARRITO ---
CARRITO_SESSION_ID = 'carrito'

# --- APPS INSTALADAS ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'catalogo.apps.CatalogoConfig',
    'carrito.apps.CarritoConfig',
    'ordenes.apps.OrdenesConfig',
    'widget_tweaks',
    'mathfilters',
]

SITE_ID = 1

LOGIN_REDIRECT_URL = '/catalogo/'
LOGOUT_REDIRECT_URL = '/account/login/'

# --- MIDDLEWARE ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mi_aplication.urls'

# --- TEMPLATES ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'catalogo.context_processors.processors.categorias_visibles',
                'carrito.context_processors.carrito',
            ],
        },
    },
]

WSGI_APPLICATION = 'mi_aplication.wsgi.application'

# --- BASE DE DATOS ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tienda_mascotas_db',
        'USER': 'postgres',
        'PASSWORD': '1929',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# --- VALIDACIÓN DE CONTRASEÑAS ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- INTERNACIONALIZACIÓN ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- ARCHIVOS ESTÁTICOS ---
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# --- ARCHIVOS DE MEDIOS ---
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# --- CONFIGURACIÓN DE STRIPE ---
STRIPE_PUBLISHABLE_KEY = 'pk_test_*********************************'
STRIPE_SECRET_KEY = 'sk_test_*********************************'
STRIPE_WEBHOOK_SECRET = 'whsec_xxxxxxxxxxxxxxxxxxxxxxxxxxx'
STRIPE_PUBLIC_KEY = "tu_clave_publica"

# --- CONFIGURACIÓN DE ALLAUTH ---
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGIN_METHODS = ['email', 'username']
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']
ACCOUNT_EMAIL_VERIFICATION = 'none'

ACCOUNT_FORMS = {
    'signup': 'mi_aplication.forms.RegistroForm',
    'login': 'mi_aplication.forms.CustomLoginForm',  # RUTA CORREGIDA
}

# --- CONFIGURACIÓN ADICIONAL ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# settings.py

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST_USER = "ep847020@gmail.com"
EMAIL_HOST_PASSWORD = "gwgp qdwp xzpd sbgd"

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
