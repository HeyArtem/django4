from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-@&76=dcbe#k=3$+qm(y0pbt5^x#%txb*bd##*@5j965bmrr3*d'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False
# ALLOWED_HOSTS = []

ALLOWED_HOSTS = ['127.0.0.1']
DEBUG = True

INTERNAL_IPS = ["127.0.0.1"]    # django-toolbar

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',  # что бы django подключал статич ф к проекту
    'django_extensions',  # Расширение для удобства работы в терминале с БД
    'women.apps.WomenConfig',
    'users',   # Авторизация и регистрация пользователей
    'debug_toolbar',    # django-toolbar
    'social_django',    # Аутентификация через соц.сети
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', # Авторизация и регистрация пользователей
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Авторизация и регистрация пользователей
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # django-toolbar
]

ROOT_URLCONF = 'sitewomen.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',  # templates/base.html
        ],  # Позволяет прописывать НЕстандартные пути к файлам шаблона
        'APP_DIRS': True,  # Говорит, что шаблоны нужно искать в директории templates. Если False-не найдет шаблон+django-toolbar
        'OPTIONS': {
            'context_processors': [         # Шаблонные Контекстные Процессоры
                'django.template.context_processors.debug',
                'django.template.context_processors.request',   # ШКП обеспечивает переменной переме-ой request, внутри шаблонов
                'django.contrib.auth.context_processors.auth',  # ШКП дает мне user в html, изпользую при отображении  Войти или Зарегаться
                'django.contrib.messages.context_processors.messages',
                'users.context_processors.get_women_context',   # Мой Шаблонный Контекстный Процессор (menu) [users-приложение, context_processors-фаил]
            ],
        },
    },
]

WSGI_APPLICATION = 'sitewomen.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# префикс для всех статич-их файлов котор будут использоваться в документе
STATIC_URL = 'static/'

# Кастомизирую панель админки, подключаю доп стили
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
# на уровне всего проекта укажу папку Где будут сохраняться все загружаемые файлы
MEDIA_ROOT = BASE_DIR / 'media'

# Что бы выводились на стр фото, а не ссылки
MEDIA_URL = '/media/'

# Тестово переношу static и прописываю новый путь
# STATICFILES_DIRS = [ BASE_DIR / 'sitewomen/static']

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Куда перенаправить пользователя после успешной авторизации
LOGIN_REDIRECT_URL = 'home'

# задает url-адрес, на котор перена-ть пользо-ля после выхода
LOGOUT_REDIRECT_URL = 'home'

# Куда, перевести незареганного пользователя, при посещении закрытой страницы.
# Альтернатива: @login_required(login_url='/admin/') (in women/views.py)
LOGIN_URL = 'users:login'

# Бэкенд аутентификации пользователя (стандартный и мой)
AUTHENTICATION_BACKENDS = [
    "social_core.backends.github.GithubOAuth2",  # Автори-я пользов-ля через github
    "django.contrib.auth.backends.ModelBackend", # Стандартный бекенд, авторизирует по username&password
    "users.authentication.EmailAuthBackend" # авторизирует по e-mail. Из прилож users, обращаюсь к моему классу EmailAuthBackend
]

# Консольный бэкенд, для восстановления пароля
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# smtp backend
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# Адрес почтового сервера
EMAIL_HOST = 'smtp.yandex.ru'
# Порт
EMAIL_PORT = '465'
# Текущий мэил адрес
EMAIL_HOST_USER = 'maidanoff.artem@yandex.ru'
# Пароль для SMTP сервера
EMAIL_HOST_PASSWORD = 'XXXXXXXXXX'
# Использовать ssl
EMAIL_USE_SSL = True

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_ADMIN = EMAIL_HOST_USER

# Подключаю модель абстрактного юзера (приложение users, User имя используемой модели в текущем проекте фреймворка Django.)
# По умолчанию было 'auth.User' (auth-берется из модуля аутентификации)
AUTH_USER_MODEL = 'users.User'

# Ава пользователя по умолчанию. MEDIA_URL-папка media и т.д.
DEFAULT_USER_IMAGE = MEDIA_URL + 'users/default.png'