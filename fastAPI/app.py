from fastapi import FastAPI
from pydantic import BaseModel
import pickle
from typing import Optional
from pathlib import Path

# Конфигурация пути
BASE_DIR = Path(__file__).resolve().parent

# Загрузка модели и энкодеров
with open(BASE_DIR / "models/linear_regression_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

with open(BASE_DIR / "models/label_encoders.pkl", "rb") as encoder_file:
    label_encoders = pickle.load(encoder_file)

# Инициализация приложения FastAPI
app = FastAPI()

# Модель данных для входного запроса
class PredictionRequest(BaseModel):
    Age_Group_Targeted: Optional[str]
    Platform: Optional[str]
    Requires_Special_Device: Optional[str]
    Price: float = 0
    Release_Year: int = 0
    Game_Length_Hours: float = 0
    Min_Number_of_Players: int = 0

# Эндпоинт для предсказания
@app.post("/predict")
async def predict(data: PredictionRequest):
    try:
        # Преобразование входных данных
        input_data = []
        for col, encoder in label_encoders.items():
            value = getattr(data, col.replace(' ', '_'), None)
            if value is not None:
                input_data.append(encoder.transform([value])[0])
            else:
                input_data.append(0)  # Значение по умолчанию

        # Добавляем числовые значения
        numeric_values = [
            data.Price,
            data.Release_Year,
            data.Game_Length_Hours,
            data.Min_Number_of_Players,
        ]
        input_data.extend(numeric_values)

        # Предсказание
        prediction = model.predict([input_data])[0]

        return {"prediction": prediction}

    except Exception as e:
        return {"error": str(e)}
