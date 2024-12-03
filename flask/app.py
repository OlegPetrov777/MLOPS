from flask import Flask, request, render_template
import pickle
import numpy as np

# Загрузка модели и энкодеров
with open('./models/linear_regression_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('./models/label_encoders.pkl', 'rb') as encoder_file:
    label_encoders = pickle.load(encoder_file)

# Инициализация приложения Flask
app = Flask(__name__)

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
            # Используем значение по умолчанию, если ключ отсутствует
            value = user_input.get(col, None)
            if value is not None:
                input_data.append(encoder.transform([value])[0])
            else:
                input_data.append(0)  # Значение по умолчанию для пропущенного

        # Добавляем остальные числовые значения
        numeric_features = ['Price', 'Release Year', 'Game Length (Hours)', 'Min Number of Players']
        for col in numeric_features:
            value = user_input.get(col, 0)  # Значение по умолчанию для пропущенного
            input_data.append(float(value))

        # Предсказание
        prediction = model.predict([input_data])[0]

        return render_template('index.html', prediction=f"Предсказанный рейтинг: {prediction:.2f}")
    except Exception as e:
        return render_template('index.html', prediction=f"Произошла ошибка: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
