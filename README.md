# TestTaskDeribitClient
Сервис на FastAPI для получения и обработки цен крпитовалют с биржи Deribit
Приложение каждую минуту получает index price для BTC и ETH через API Deribit, сохраняет данные в PostgreSQL и предоставляет внешнее API для работы с сохранёнными значениями.

# Функциональность
* периодическое получение цен BTC и ETH с Deribit
* ранение тикера, цены и времени в формате UNIX timestamp в PostgreSQL
* REST API для:
  * получения всех сохранённых данных по валюте 
  * получения последней цены валюты 
  * получения цены валюты за указанный период 
  * миграции базы данных через Alembic 
  * фоновое выполнение периодических задач через Celery + Redis 
  * запуск приложения через Docker Compose

# Используемые технологии
* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* Alembic
* Celery
* Redis
* Docker
* Docker Compose

## Запуск проекта локально
### 1. Клонирование репозитория
```bash
git clone https://github.com/AlexGitHub21/TestTaskDeribitClient.git
cd TestTaskDeribitClient
````

### 2. Установка зависимостей
```bash
pip install -r requirements.txt
```
### 3. Настройка переменных окружения
Создать файл .env в корне проекта и указать параметры подключения к PostgreSQL и Redis. Создать базу данных PostgreSQL
```env
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
DB_ECHO=

REDIS_HOST=
REDIS_PORT=

CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
APP_HOST_PORT=5050
```

### 4. Миграции БД
Если нужно создать новую миграцию, тогда шаг 4.1 и 4.2
Если миграция есть, достаточно применить ее, шаг 4.2
#### 4.1. Создать миграцию
```commandline
alembic revision --autogenerate -m "Create Table"
```
#### 4.2 Примернить миграцию
```commandline
alembic upgrade head
```

### 5. Запуск приложения (не Docker)


В корне проекта прописать команду:
```bash
uvicorn main:app --reload
```

### 5. Открыть Swagger UI (документацию)
http://127.0.0.1:8000/docs

### 6. Запустить redis (брокер задач)
В терминале в корне проекта:
``` bash
redis-server 
```

### 7. Запустить celery (воркер задач)
В терминале в корне проекта:
```commandline
celery -A app.celery_app worker -l INFO
```
-l INFO выводит в консоль информационные сообщения о выполняемых процессах

### 8. Запустить celery (планировщик задач)
В терминале в корне проекта:
```commandline
celery -A app.celery_app beat --loglevel=info
```
Celery Beat отвечает за периодический запуск задачи, которая получает актуальные цены с Deribit и сохраняет их в базу данных.

## Запустить через Docker 

***Собрать Docker-образ***
```commandline
docker compose build
```

***Миграция БД***
```
docker compose run --rm app bash
alembic -c alembic.ini revision --autogenerate -m "Initial migration"
alembic -c alembic.ini upgrade head
exit
```

***Запустить контейнеры***
```commandline
docker compose up -d
```

### API-методы
Получить цены по валюте (BTC, ETH)
```commandline
GET /prices/?ticker=
```

Получить последнюю цену валюты (BTC, ETH)
```commandline
GET /prices_latest/?ticker=
```
Получить цены за период
```commandline
GET /prices/by_date?ticker=&from_ts=&to_ts=
```

***Остановить контейнеры***
```commandline
docker compose down -v
```

### Design decisions
* Для веб-API был выбран FastAPI, так как он удобно поддерживает асинхронные обработчики, dependency injection и автоматически генерирует Swagger-документацию.
* Для работы с базой данных использован PostgreSQL.
* Для ORM использован SQLAlchemy с асинхронными сессиями.
* Для хранения истории изменения цен выбрана отдельная таблица со значениями ticker, price, timestamp.
* Для периодического получения данных использован Celery Beat, а Redis выступает брокером сообщений.
* SQLAlchemy engine и session factory создаются один раз на уровне приложения, а для каждой операции создаётся отдельная сессия.
* Для управления схемой базы данных используются миграции Alembic.
* Docker Compose используется для упрощения локального развёртывания приложения и зависимостей.

#### Просмотреть что в БД сохраняютcя данные
```commandline
docker exec -it deribit_client_db bash  # открыть терминал внутри контейнера базы данных
psql -U <DB_USER> -d <DB_NAME>          # подключиться к PostgreSQL
\dt                                     # посмотреть доступные таблицы
SELECT * FROM <название таблицы>;       # проверить сохранённые данные
\q                                      # выйти из клиента PostgreSQL
```


