FROM python:3.11.5-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Сначала копируем только requirements.txt для лучшего использования кеша слоев
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Затем копируем остальные файлы
COPY . .

CMD ["sh", "-c", "echo 'Sleeping 5 seconds...'; sleep 5; alembic upgrade head && python main.py"]
