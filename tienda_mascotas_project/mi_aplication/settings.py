
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
ALLOWED_HOSTS = [ '.onrender.com', 'localhost', '127.0.0.1']

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
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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
