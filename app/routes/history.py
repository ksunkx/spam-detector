import logging
from fastapi import APIRouter, HTTPException
from app.db import get_connection

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/history")
def get_history():
    """Возвращает последние 20 запросов из базы данных."""
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM requests_history ORDER BY created_at DESC LIMIT 20"
            )
            rows = cur.fetchall()
        conn.close()
        return list(rows)
    except Exception as e:
        logger.error(f"Ошибка получения истории: {e}")
        raise HTTPException(status_code=500, detail="Ошибка подключения к базе данных.")


@router.get("/history/{item_id}")
def get_history_item(item_id: int):
    """Возвращает один запрос по его id."""
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM requests_history WHERE id = %s", (item_id,)
            )
            row = cur.fetchone()
        conn.close()
    except Exception as e:
        logger.error(f"Ошибка получения записи {item_id}: {e}")
        raise HTTPException(status_code=500, detail="Ошибка подключения к базе данных.")

    if row is None:
        raise HTTPException(status_code=404, detail=f"Запись с id={item_id} не найдена.")

    return row
