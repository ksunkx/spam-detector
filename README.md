# AI Spam Detector API

REST API для классификации текста как SPAM / NOT SPAM с использованием Hugging Face модели.

## Стек технологий

- Python + FastAPI
- PostgreSQL
- Docker / Docker Compose
- Hugging Face Transformers
- Postman

## Быстрый старт

### 1. Клонировать репозиторий

```bash
git clone https://github.com/ВАШ_ЛОГИН/spam-detector.git
cd spam-detector
```

### 2. Создать файл .env

```bash
cp .env.example .env
```

### 3. Запустить через Docker Compose

```bash
docker compose up --build
```

Первый запуск займёт несколько минут (скачивается модель ~50MB).

### 4. Проверить работу

Открыть браузер: http://localhost:8000/health

Ответ: `{"status": "ok"}`

Swagger документация: http://localhost:8000/docs

---

## API Endpoints

| Метод | URL | Описание |
|-------|-----|----------|
| GET | /health | Проверка доступности |
| POST | /analyze | Анализ текста |
| GET | /history | Последние 20 запросов |
| GET | /history/{id} | Запрос по ID |

### POST /analyze

Запрос:
```json
{"text": "Congratulations! You won a FREE iPhone!"}
```

Ответ:
```json
{"result": "SPAM", "score": 0.98, "model": "mrm8488/bert-tiny-finetuned-sms-spam-detection"}
```

---

## Тестирование через Postman

1. Открыть Postman
2. Import → выбрать файл `postman/collection.json`
3. Запустить запросы

---

## Структура проекта

```
project/
├── app/
│   ├── main.py        # Точка входа FastAPI
│   ├── db.py          # Подключение к PostgreSQL
│   ├── ml_service.py  # Работа с Hugging Face
│   ├── schemas.py     # Модели данных
│   └── routes/
│       ├── analyze.py # POST /analyze
│       └── history.py # GET /history
├── postman/
│   └── collection.json
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```
