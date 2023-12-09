# Store - интернет магазин

Проект - интернет магазина, в котором пользователи могут выбирать товары из каталога, добавлять в корзину и 
оформлять заказы.

**Стек:**
+ [Python](https://www.python.org/downloads/) (Django)
+ [PostgreSQL](https://www.postgresql.org/)
+ [Redis](https://redis.io/)
+ [Celery](https://docs.celeryq.dev/en/stable/index.html#)
+ [Stripe](https://dashboard.stripe.com/test/dashboard) 
+ [OAuth 2.0 - django allauth](https://docs.allauth.org/en/latest/)

В проекте реализованы:
+ возможность оформление товаров (произведение оплаты), добавленных в корзину через платежную систему Stripe
+ подключен webhook Stripe для отлавливания результата оплаты и дальней обработки
+ авторизация через GitHub, с помощью протокола OAuth 2.0 (с использованием django-allauth)
+ кеширование с использованием Redis
+ отложенная задача с использованием Celery + Redis по отправке письма на почту (Yandex SMTP) пользователя для подтверждения учетной записи

## Локальная разработка:

Все действия должны выполняться из исходного каталога проекта и только после установки всех требований.

1. Во-первых, создайте и активируйте новую виртуальную среду:

```shell
python -m venv venv
venv\Scripts\activate
```

2. Установите пакеты:

```shell
pip install --upgrade pip
pip install -r requirements.txt
```

3. Запуск зависимостей проекта, миграции, заполнение базы данных данными о товарах и т.д.:

```shell
python manage.py migrate
python manage.py loaddata <path_to_fixture_files>
```
**Примечание 1:** файлы фикстур в проекте находятся по следующим путям:
+ products/fixtures/categories.json
+ products/fixtures/products.json
+ users/fixtures/users.json

**Примечание 2:** после загрузки фикстур может потребоваться выполнить команды:

```shell
python manage.py makemigration 
python manage.py migrate
```

4. Запустите Redis: [инструкция по запуску](https://redis.io/docs/install/install-redis/).


5. Запустите сервер:
```shell
python manage.py runserver
```

6. Запустите **Celery** для проверки работы отложенной задачи по отправке письма с подтверждением регистрации:

   + если вы используете ОС Windows, необходимо запустить через eventlet (в связи с тем, что пул параллелизма по умолчанию prefork не работает в Windows):

    ```shell
    celery -A store worker --loglevel=info -P eventlet
    ```

   + если другую ОС:

    ```shell
      celery -A store worker -l INFO
    ```

7. Для работы со **Stripe** необходимо выполнить [авторизацию](https://stripe.com/docs/stripe-cli). Поскольку для авторизации необходим **секретный ключ**, то
файл **.env** не был добавлен в **gitignore**. Выполните следующую команду, взяв ключ из файла **.env**:

```shell
.\stripe login --interactive
Enter your API key: stripe_secret_key
```

Далее необходимо подключить **webhook**:

```shell
 .\stripe listen --forward-to 127.0.0.1:8000/webhook/stripe/
```

**Примечание:** для **оплаты товара** используйте тестовый номер карты (для успешной оплаты): **4242424242424242**, **год** 
срока карты должен быть выше **текущего года**. Остальные данные могут быть произвольные.
