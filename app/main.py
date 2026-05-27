import logging
from fastapi import FastAPI
from app.db import create_table
from app.routes import analyze, history

# Настройка логирования — записывает события в консоль
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Spam Detector API")

# При старте приложения создаём таблицу в БД (если её ещё нет)
@app.on_event("startup")
async def startup():
    logger.info("Сервис запускается...")
    create_table()
    logger.info("Таблица БД готова.")

# Подключаем роутеры (файлы с endpoints)
app.include_router(analyze.router)
app.include_router(history.router)

# Endpoint проверки доступности сервиса
@app.get("/health")
def health_check():
    return {"status": "ok"}
