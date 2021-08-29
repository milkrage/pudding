# Pudding
It's a password manager with AES on the client side.<br>
Demo stand: https://pudding.milkrage.ru

## Install

### Install venv
1. `python -m venv pudding`
2. `cd pudding`
3. for Windows: `Scripts\activate.bat`

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
# change YOURKEY 
# example: 'django-insecure-izda&@s9k5o*gbkw_ci&zau_#p++&kg-=-)=9w-db)mm2+i2gn'
SECRET_KEY = 'django-insecure-YOURKEY'

DEBUG = False
ALLOWED_HOSTS = []
REQUIRE_HTTPS = False
```

### Initialize database
1. `cd app`
2. `python manage.py makemigrations`
3. `python manage.py migrate`

### Run
1. `python manage.py runserver`