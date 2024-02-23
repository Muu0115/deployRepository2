# local_settings.py

DEBUG = True

# ローカルデータベース設定
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase',
    }
}

ALLOWED_HOSTS = [‘*’]
# その他ローカル環境専用の設定...
