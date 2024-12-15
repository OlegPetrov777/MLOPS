from flask import Flask, request, render_template, g
import pickle
import sqlite3
import os
import subprocess


# Загрузка модели и энкодеров
with open('/app/models/linear_regression_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('/app/models/label_encoders.pkl', 'rb') as encoder_file:
    label_encoders = pickle.load(encoder_file)

# Конфигурация БД
DATABASE = 'logs.db'

# Инициализация приложения Flask
app = Flask(__name__)

# Функция для создания БД при отсутствии
def initialize_db():
    if not os.path.exists(DATABASE):
        print("Инициализация базы данных...")
        subprocess.run(["python", "init_db.py"])

# Функция для подключения к БД
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Главная страница
@app.route('/')
def home():
    return render_template('index.html')

# Обработка предсказания
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Получаем данные из формы
        user_input = request.form

        # Преобразуем входные данные
        input_data = []
        for col, encoder in label_encoders.items():
            value = user_input.get(col, None)
            if value is not None:
                input_data.append(encoder.transform([value])[0])
            else:
                input_data.append(0)  # Значение по умолчанию

        # Добавляем числовые значения
        numeric_features = ['Price', 'Release Year', 'Game Length (Hours)', 'Min Number of Players']
        numeric_values = []
        for col in numeric_features:
            value = user_input.get(col, 0)
            numeric_values.append(float(value))
            input_data.append(float(value))

        # Предсказание
        prediction = model.predict([input_data])[0]

        # Логирование в БД
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO logs (age_group, platform, special_device, price, release_year, game_length, min_players, prediction)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_input.get('Age Group Targeted', ''),
              user_input.get('Platform', ''),
              user_input.get('Requires Special Device', ''),
              numeric_values[0],  # Price
              int(numeric_values[1]),  # Release Year
              numeric_values[2],  # Game Length
              int(numeric_values[3]),  # Min Number of Players
              prediction))
        db.commit()

        return render_template('index.html', prediction=f"Предсказанный рейтинг: {prediction:.2f}")

    except Exception as e:
        return render_template('index.html', prediction=f"Произошла ошибка: {str(e)}")

# Маршрут для просмотра логов
@app.route('/logs')
def view_logs():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM logs')
    logs = cursor.fetchall()
    return render_template('logs.html', logs=logs)

if __name__ == '__main__':
    initialize_db()  # Проверка и инициализация БД
    app.run(host="0.0.0.0", port=5000, debug=True)
