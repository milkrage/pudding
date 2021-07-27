app/settings.py:
* SECRET_KEY и DEBUG хранятся в app/environment.py (добавлен в .gitignore)
* добавил PROJECT_DIR, используется в адресе сохранения БД
* из INSTALLED_APPS убран 'django.contrib.admin'
* для переопределения User и UserManager установлена константа AUTH_USER_MODEL = 'pudding.User'

планы краткосрочные:
  * разобраться с генирацией файлов локализации (gettext_lazy)
  * сделать форму аутентификации и регистрации 
 
 планы среднесрочные:
 * описать модели для хранения ключей (паролей): www / app / ssh