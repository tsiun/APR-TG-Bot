# Используем официальный Python образ (совместим с PTB 20.8)
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей и устанавливаем библиотеки
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё остальное
COPY . .

# Запуск приложения
CMD ["python", "APRbot.py"]