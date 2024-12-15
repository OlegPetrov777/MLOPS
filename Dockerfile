# Используем базовый образ с Python
FROM python:3.11.9

# Обновляем pip, setuptools и wheel
RUN pip install --upgrade pip setuptools wheel

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы в контейнер
COPY . /app

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Открываем порт, на котором будет работать приложение
EXPOSE 5000

# Команда для запуска Flask-приложения
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
