# Cервис Marketplace

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/-FastAPI-464646?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Асинхронность](https://img.shields.io/badge/-Асинхронность-464646?style=flat-square&logo=Асинхронность)]()
[![Cookies](https://img.shields.io/badge/-Cookies-464646?style=flat-square&logo=Cookies)]()
[![JWT](https://img.shields.io/badge/-JWT-464646?style=flat-square&logo=JWT)]()
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Alembic](https://img.shields.io/badge/-Alembic-464646?style=flat-square&logo=Alembic)](https://alembic.sqlalchemy.org/en/latest/)
[![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy-464646?style=flat-square&logo=SQLAlchemy)](https://www.sqlalchemy.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![Redis](https://img.shields.io/badge/-Redis-464646?style=flat-square&logo=Redis)](https://redis.io/)
[![Celery](https://img.shields.io/badge/-Celery-464646?style=flat-square&logo=Celery)](https://docs.celeryq.dev/en/stable/)
[![Sentry](https://img.shields.io/badge/-Sentry-464646?style=flat-square&logo=Sentry)](https://sentry.io/welcome/)
[![Prometheus](https://img.shields.io/badge/-Prometheus-464646?style=flat-square&logo=Prometheus)](https://prometheus.io/)
[![Grafana](https://img.shields.io/badge/-Grafana-464646?style=flat-square&logo=Grafana)](https://grafana.com/)
[![Uvicorn](https://img.shields.io/badge/-Uvicorn-464646?style=flat-square&logo=uvicorn)](https://www.uvicorn.org/)
[![Gunicorn](https://img.shields.io/badge/-Gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)

## Описание

API онлайн-магазина бытовой техники.

### Доступный функционал

- Регистрация пользователей с помощью библиотеки fastapi-users.
- Аутентификация реализована с помощью куков и JWT-токена.
- У неаутентифицированных пользователей доступ к API только на уровне чтения.
- Создание объектов разрешено только аутентифицированным пользователям.
- Возможность получения подробной информации о себе.
- Загрузка тестовых данных в БД.
- Возможность осуществить операции CRUD для категорий.
- Возможность получить список всех товаров подкатегории и выполнить операции CRUD.
- Возможность получить подробную информацию о товаре и выполнить операции CRUD.
- Отправка email с подтверждением покупки пользователя посредством Celery.
- Возможность администрирования сервиса.
- Версионирование API.
- Кеширование/брокер задач с помощью Redis.
- Логирование посредством кастомного логгера.
- Мониторинг ошибок с помощью Sentry.
- Сбор метрик с помощью Prometheus.
- Визуализация метрик посредством Grafana.
- Возможность развернуть проект в Docker-контейнерах.

#### Локально документация доступна по адресу: <http://localhost:8000/v1/docs/>
#### В контейнерах Docker документация доступна по адресу: <http://localhost:7777/v1/docs/>  

#### Технологии

- Python 3.9
- FastAPI
- fastapi-cache2
- Асинхронность
- Cookies
- JWT
- Alembic
- SQLAlchemy
- Docker
- PostgreSQL
- Asyncpg
- CORS
- Redis
- Celery
- Flower
- Sentry
- Prometheus
- Grafana
- Uvicorn
- Gunicorn

#### Локальный запуск проекта

- Предварительно необходимо установить Docker и Redis для вашей системы.

- Склонировать репозиторий:

```bash
    git clone <название репозитория>
```

Cоздать и активировать виртуальное окружение:

Команды для установки виртуального окружения на Mac или Linux:

```bash
    python3 -m venv env
    source env/bin/activate
```

Команды для Windows:

```bash
    python -m venv venv
    source venv/Scripts/activate
```

- Перейти в директорию app:

```bash
    cd /app
```

- Создать файл .env по образцу:

```bash
    cp .env-local-example .env
```

- Установить зависимости из файла requirements.txt:

```bash
    cd ..
    pip install -r requirements.txt
```

- Для создания миграций выполнить команду:

```bash
    alembic init migrations
```

- В папку migrations в env файл вставьте следующий код:

```bash
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.categories.models import Category
from app.config import settings
from app.database.db import Base
from app.goods.models import Goods
from app.purchases.models import Purchase
from app.subcategories.models import Subcategory
from app.users.models import User

config = context.config

config.set_main_option('sqlalchemy.url', f'{settings.DATABASE_URL}?async_fallback=True')

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata
```

- Инициализировать БД:

``` bash
    alembic revision --autogenerate -m "comment"   
```

- Применить миграцию:

``` bash
    alembic upgrade head 
```

- Запустить проект:

``` bash
    uvicorn app.main:app --reload    
```

- Запустить Redis:

``` bash
    redis-server.exe 
    redis-cli.exe  
```

- Запустить Celery:

``` bash
    celery -A app.tasks.celery:celery worker --loglevel=INFO --pool=solo
```

- Запустить Flower: 

``` bash
    celery -A app.tasks.tasks:celery flower
```

#### Запуск в контейнерах Docker

- Находясь в главной директории проекта:

- Создать файл .env-docker по образцу:

```bash
   cp .env-docker-example .env-docker 
```

- Запустить проект:

``` bash
    docker-compose up -d --build  
```

#### Примеры некоторых запросов API

Регистрация пользователя:

```bash
   POST /users/register
```

Получение данных своей учетной записи:

```bash
   GET /users/me 
```

Добавление покупки:

```bash
   POST /purchases
```

Получение списка категорий:
  
```bash
   GET /categories 
```

Получение списка всех товаров подкатегории:

```bash
   GET /subcategories/{subcategory_id}/goods
```

Загрузка тестовых данных:

```bash
   POST /import/{table_name}
```

#### Полный список запросов API находится в документации

#### Автор

Гут Владимир - [https://github.com/VladimirMonolith](http://github.com/VladimirMonolith)
