# MLOps

## О курсе

Методы машинного обучения и искусственного интеллекта давно стали частью нашей жизни. Эти технологии используются для создания интеллектуальных информационных систем, работающих в самых разных областях. Однако построение качественной модели — это лишь первый шаг. Для полноценной эксплуатации необходимо интегрировать модель в существующую информационную систему.

**MLOps** — это набор практик и методов управления жизненным циклом моделей машинного обучения. Эти практики включают:

- Моделирование жизненного цикла и управление рисками;
- Интеграцию моделей в прикладные приложения;
- Автоматизацию процессов версионирования, мониторинга и развертывания.

MLOps позволяет сделать процесс работы с моделями машинного обучения более эффективным и надежным.

---

## Структура проекта

### `ml-ops.ipynb`
Jupyter Notebook, предназначенный для анализа данных и построения модели машинного обучения. В качестве данных используется датасет с обзорами и рейтингами видеоигр.

### `models/`
Папка, содержащая сохраненные обученные модели, созданные в процессе работы с `ml-ops.ipynb`.

### `app.py`
Приложение на Flask, реализующее API для выполнения предсказаний на основе модели линейной регрессии, загружаемой из внешнего файла.

### `templates/`
Папка с HTML-шаблонами, используемыми Flask-приложением для отправки клиенту (браузеру) визуализированных данных.

---

## Docker-экосистема

### `docker-compose.yml`
Конфигурационный файл для Docker Compose, обеспечивающий запуск многоконтейнерного приложения. Основные параметры:

- **`version`**: Версия конфигурации (`3`).
- **`services`**: Определяет сервисы приложения. В данном случае — сервис `flask-app`.
- **`build`**: Контекст сборки — текущая директория (`.`).
- **`ports`**: Связывает порт хоста `5000` с портом контейнера `5000` для доступа к приложению.
- **`volumes`**: Монтирует текущую директорию хоста в директорию `/app` контейнера, что упрощает разработку.
- **`environment`**: Задает переменные окружения, включая:
  - `FLASK_ENV=development` — режим разработки;
  - `FLASK_RUN_HOST=0.0.0.0` — прием запросов со всех сетевых интерфейсов.

### `Dockerfile`
Файл для создания Docker-образа Flask-приложения. Основные шаги:

1. **`FROM python:3.11.9`**: Используется образ Python версии 3.11.9.
2. **`RUN pip install --upgrade pip setuptools wheel`**: Обновление пакета `pip` и инструментов.
3. **`WORKDIR /app`**: Установка рабочей директории `/app`.
4. **`COPY . /app`**: Копирование всех файлов в контейнер.
5. **`RUN pip install -r requirements.txt`**: Установка зависимостей.
6. **`EXPOSE 5000`**: Открытие порта `5000`.
7. **`CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]`**: Запуск Flask-приложения.

---

## Итоги

Эта структура проекта и файлы позволяют:

1. Разрабатывать и тестировать модели машинного обучения в Jupyter Notebook.
2. Интегрировать модели в веб-приложение на Flask.
3. Развертывать приложение в изолированной среде с использованием Docker и Docker Compose.

Для запуска проекта используйте команду:

```bash
docker-compose up
