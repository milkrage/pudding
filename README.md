# Pudding
It's a password manager with AES on the client side.<br>
Demo stand: https://pudding.milkrage.ru

## Install

### Install virtual environments
1. `mkdir pudding`
2. `cd pudding`
3. `python -m venv ./venv`
4. `source venv/bin/activate`

### Download
1. `git init` 
2. `git remote add origin https://github.com/milkrage/pudding.git`
3. `git pull origin master`

### Install requirements
1. `pip install -r requirements.txt`

### Create config
1. `cd app/app`
2. `touch environment.py`

Generate SECRET_KEY: <br>
`python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`

Example environment.py:
```
# Security
# change YOURKEY in SECRET_KEY
# example: 'django-insecure-izda&@s9k5o*gbkw_ci&zau_#p++&kg-=-)=9w-db)mm2+i2gn'
DEBUG = False
SECRET_KEY = 'django-insecure-YOURKEY'
ALLOWED_HOSTS = []

# URL config
REQUIRE_HTTPS = False
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Static files
STATIC_ROOT = None

# API Settings
API_ENABLE = True
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ]
}

# Database example:
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

```

### Initialize database
1. `cd pudding/app`
2. `python manage.py makemigrations`
3. `python manage.py migrate`

### Run
1. `python manage.py runserver`
