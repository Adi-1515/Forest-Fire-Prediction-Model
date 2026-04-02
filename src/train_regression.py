import pickle
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from src.data_preprocessing import load_and_preprocess_data
from src.utils import get_model_path

def train():
    print("Loading data for regression...")
    X, y_reg, y_clf = load_and_preprocess_data()
    
    X_train, X_test, y_train, y_test, y_class_train, y_class_test = train_test_split(
        X, y_reg, y_clf, train_size=0.8, random_state=42
    )
    
    # Train purely on regions where fire occurred
    X_train_fire = X_train[y_class_train == 1]
    y_train_fire = y_train[y_class_train == 1]
    X_test_fire = X_test[y_class_test == 1]
    y_test_fire = y_test[y_class_test == 1]

    print("Training Regressor with GridSearch...")
    param_grid_reg = {
        'n_estimators': [50, 100],
        'max_depth': [2, 3],
        'min_samples_split': [15, 20],
        'min_samples_leaf': [10, 20]
    }
    gs_reg = GridSearchCV(RandomForestRegressor(random_state=42), 
                          param_grid_reg, cv=3, scoring='r2', n_jobs=-1)
    gs_reg.fit(X_train_fire, y_train_fire)
    rf_model = gs_reg.best_estimator_

    # Evaluation
    y_pred_fire = rf_model.predict(X_test_fire)
    
    mae = mean_absolute_error(y_test_fire, y_pred_fire)
    mse = mean_squared_error(y_test_fire, y_pred_fire)
    r2 = r2_score(y_test_fire, y_pred_fire)

    print("\n--- Regressor Results ---")
    print(f"MAE: {mae:.2f}")
    print(f"MSE: {mse:.2f}")
    print(f"R² Score: {r2:.2f}")
    print(f"Best Params: {gs_reg.best_params_}")

    out_path = get_model_path('regression_model')
    with open(out_path, "wb") as f:
        pickle.dump(rf_model, f)
    print(f"Model successfully saved to {out_path}\n")

if __name__ == "__main__":
    train()
