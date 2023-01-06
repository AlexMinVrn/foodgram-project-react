# foodgram-project «Продуктовый помощник»

### Админ - admin
### Пароль - qwer@1234
### Описание
На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других  
пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин  
скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
#### >Сервис размещен на сервере Yandex Cloud и доступен по адресу:
#### >http://51.250.66.16/recipes
### Техническое описание

К проекту по адресу http://51.250.66.16/api/docs/ подключена документация API Foodgram.  
В ней описаны возможные запросы к API и структура ожидаемых ответов. Для каждого запроса  
указаны уровни прав доступа.
### Уровни доступа пользователей:
- **Гость** (неавторизованный пользователь)
- **Авторизованный пользователь**
- **Администратор**
### Технологии
- [Python] v3.7
- [Django] v2.2.16
- [Django REST framework] v3.12.4
- [Docker]
- Gunicorn
- nginx
### Запуск проекта
### Клонируйте проект и задайте настройки, для этого:

#### Подключитесь к своему серверу
ssh <server user>@<server IP>
Например: ssh root@00.000.00.00

#### Клонируйте проект на сервер:
git@github.com:AlexMinVrn/foodgram-project-react.git

#### Подготовьте дополнительные данные (.env и nginx.conf):

##### Скопируйте в директорию проекта infra/ файл nginx.conf 

##### В файле nginx.conf в строке server_name укажите данные ip вашего сервера.

##### Создайте в директории проекта infra/ файл .env и наполните его следующими данными
DEBUG=False  
SECRET_KEY=<Длинная строка с латинскими буквами, цифрами и символами>  
DB_ENGINE='django.db.backends.postgresql'  
DB_NAME='postgres'  
POSTGRES_USER='postgres'  
POSTGRES_PASSWORD=<Ваш пароль>  
DB_HOST='db'  
DB_PORT=5432  

#### Подготовьте сервер для работы с проектом:

##### Установите docker и docker-compose:
sudo apt install docker.io  
sudo apt install docker-compose

##### Соберите контейнерs:

sudo docker-compose up -d --build

##### Выполните миграции
sudo docker-compose exec backend python manage.py makemigrations  
sudo docker-compose exec backend python manage.py migrate

##### Создайте суперюзера:
sudo docker-compose exec backend python manage.py createsuperuser

##### Cоберите статику
sudo docker-compose exec backend python manage.py collectstatic --no-input

##### Можно работать с преподготовленными ингредиентами, для этого нужно их загрузить командой:

sudo docker-compose exec backend python manage.py importcsv

### Автор
- [Александр Минаев]

[//]: # 
  [Python]: <https://www.python.org>
  [Django REST framework]: <https://www.django-rest-framework.org>
  [Django]: <https://www.djangoproject.com>
  [JWT]: <https://jwt.io>
  [Docker]: <https://www.docker.com>
  [Pillow]: <https://pillow.readthedocs.io/>
  [Александр Минаев]: <https://github.com/AlexMinVrn>