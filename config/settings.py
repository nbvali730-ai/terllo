"""
Django settings for config project.
"""

from pathlib import Path

# مسیر اصلی پروژه
BASE_DIR = Path(__file__).resolve().parent.parent

# تنظیمات امنیتی (در حالت توسعه)
SECRET_KEY = 'django-insecure-cl6(=j$^@*95hyx(zo-b0xbt#4ag$ag^s^r2w=p*j=x2kc%i%#'
DEBUG = True
ALLOWED_HOSTS = []

# اپلیکیشن‌های نصب شده
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tasks', # اپلیکیشن مدیریت وظایف شما
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # تنظیم شده برای پوشه قالب‌ها
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

WSGI_APPLICATION = 'config.wsgi.application'

# دیتابیس (SQLite برای شروع عالی است)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# تایید اعتبار رمز عبور
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# تنظیمات زبان و زمان (به فارسی و تهران تغییر دادم)
LANGUAGE_CODE = 'fa-ir'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_TZ = True

# فایل‌های استاتیک
STATIC_URL = 'static/'

# نوع فیلد آیدی پیش‌فرض
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# ته فایل settings.py اضافه کن
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
