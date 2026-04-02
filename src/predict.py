import pickle
import numpy as np
import pandas as pd
from src.utils import get_model_path

class ForestFirePredictor:
    def __init__(self):
        self.regressor = self._load_model('regression_model')
        self.classifier = self._load_model('classifier_model')

    def _load_model(self, model_name):
        model_path = get_model_path(model_name)
        try:
            with open(model_path, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            print(f"Warning: Model {model_name} not found at {model_path}.")
            return None

    def predict(self, input_features: dict):
        """
        Predicts the probability of fire and area burned.
        Keys expected: 'X', 'Y', 'month', 'day', 'FFMC', 'DMC', 'DC', 'ISI', 'temp', 'RH', 'wind', 'rain'
        """
        if not self.regressor or not self.classifier:
            raise ValueError("Models are not loaded.")

        df_input = pd.DataFrame([input_features])
        
        # Fire occurrence probability
        prob = self.classifier.predict_proba(df_input)[0][1]
        
        # Area prediction
        log_area_pred = self.regressor.predict(df_input)[0]
        area_pred = np.expm1(log_area_pred)
        
        return {
            "fire_probability": float(prob),
            "estimated_area_burned_ha": float(area_pred) if prob > 0.5 else 0.0
        }

if __name__ == "__main__":
    # Test example
    predictor = ForestFirePredictor()
    sample_input = {
        'X': 5, 'Y': 5, 'month': 8, 'day': 4,
        'FFMC': 90.0, 'DMC': 100.0, 'DC': 500.0, 'ISI': 8.0,
        'temp': 20.0, 'RH': 50, 'wind': 5.0, 'rain': 0.0
    }
    result = predictor.predict(sample_input)
    print(f"Prediction Result: {result}")
