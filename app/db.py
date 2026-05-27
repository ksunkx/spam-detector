import os
import logging
import psycopg2
from psycopg2.extras import RealDictCursor

logger = logging.getLogger(__name__)

# Читаем URL базы данных из переменной окружения (задаётся в .env)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@postgres:5432/spamdb")


def get_connection():
    """Создаёт и возвращает соединение с PostgreSQL."""
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        logger.error(f"Ошибка подключения к БД: {e}")
        raise


def create_table():
    """Создаёт таблицу requests_history если её ещё нет."""
    sql = """
    CREATE TABLE IF NOT EXISTS requests_history (
        id SERIAL PRIMARY KEY,
        input_text TEXT NOT NULL,
        result_text TEXT NOT NULL,
        model_name VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT NOW()
    );
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()
    finally:
        conn.close()
