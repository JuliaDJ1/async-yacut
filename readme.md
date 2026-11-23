<div align="center">

# ✂️ YaCut

**Сервис коротких ссылок и файлообменник: сокращение URL, REST API и асинхронная загрузка файлов на Яндекс Диск**

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?logo=flask&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?logo=sqlalchemy&logoColor=white)
![aiohttp](https://img.shields.io/badge/aiohttp-async-2C5BB4?logo=aiohttp&logoColor=white)
![Tests](https://img.shields.io/badge/pytest-35%2F35_passed-2ea44f?logo=pytest&logoColor=white)

</div>

## О проекте

YaCut превращает длинную ссылку в короткую вида `http://host/abc123` — автоматически или с собственным идентификатором.
Вторая функция — файлообменник: пользователь загружает несколько файлов, сервис асинхронно отправляет их на Яндекс Диск и выдаёт по короткой ссылке на каждый.

## Возможности

- Веб-форма сокращения ссылок (Flask-WTF) с валидацией и пользовательским идентификатором до 16 символов (латиница и цифры).
- Генерация уникального 6-символьного идентификатора.
- **REST API** (спецификация — [`openapi.yml`](openapi.yml)): создание короткой ссылки и получение исходного URL.
- Загрузка нескольких файлов на **Яндекс Диск через aiohttp** (получение ссылки на загрузку → загрузка → получение ссылки на скачивание).
- Обработка ошибок API в едином JSON-формате, собственные страницы 404 и 500.

## Стек

Python 3.12 · Flask 3 · Flask-SQLAlchemy · Flask-Migrate (Alembic) · Flask-WTF · aiohttp · asyncio · Яндекс Диск REST API · SQLite · pytest

## Что сделано

- Модель `URLMap`, веб-представления и API-представления разделены по модулям.
- Асинхронный клиент Яндекс Диска на aiohttp, вызываемый из синхронного Flask-представления через отдельный event loop.
- Миграции базы данных через Flask-Migrate.
- **35 из 35 автотестов** проходят (Яндекс Диск подменяется mock-сервером).

## Запуск

**Требования:** Python 3.10+ (проверено на 3.12), OAuth-токен Яндекс Диска для загрузки файлов.

```bash
git clone https://github.com/vadim-guseinov/async-yacut.git
cd async-yacut
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env            # заполните SECRET_KEY и DISK_TOKEN
flask db upgrade
flask run
```

### Тесты

```bash
pytest
```

## Примеры запросов к API

```bash
curl -X POST http://127.0.0.1:5000/api/id/ \
  -H "Content-Type: application/json" \
  -d '{"url": "https://docs.python.org/3/library/asyncio.html", "custom_id": "asyncio"}'
# {"url": "https://docs.python.org/3/library/asyncio.html", "short_link": "http://127.0.0.1:5000/asyncio"}

curl http://127.0.0.1:5000/api/id/asyncio/
# {"url": "https://docs.python.org/3/library/asyncio.html"}
```

## Автор

**Вадим Гусейнов** — Python-разработчик (Backend) · [Telegram](https://t.me/eviliing)
