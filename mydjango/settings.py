import os

# 项目基础目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 安全密钥
SECRET_KEY = '(q4faq9p%p*35^7oor_g48cg2&hf-isf7f4d_9hr(@9d##am50'

# 调试模式
DEBUG = True

# 允许的主机
ALLOWED_HOSTS = ['*']

# 已安装的应用
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# 中间件配置（确保顺序正确）
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # 必须在此位置
    'django.contrib.messages.middleware.MessageMiddleware',    # 紧随其后
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 项目 URL 配置
ROOT_URLCONF = 'mydjango.urls'

# 模板配置
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # 模板目录
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

# WSGI 应用程序
WSGI_APPLICATION = 'mydjango.wsgi.application'

# 数据库配置（SQLite3）
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# 国际化配置
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# 静态文件配置
STATIC_URL = '/static/'  # 静态文件 URL 前缀
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # 项目中存放静态文件的目录
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # 用于 collectstatic 的目录

# 登录相关配置
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/travelhome'
LOGOUT_REDIRECT_URL = '/login/'
