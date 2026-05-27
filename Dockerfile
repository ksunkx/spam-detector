# Берём официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую папку внутри контейнера
WORKDIR /app

# Сначала копируем только requirements.txt (чтобы не переустанавливать при каждом билде)
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь остальной код
COPY . .

# Запускаем FastAPI через uvicorn на порту 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
