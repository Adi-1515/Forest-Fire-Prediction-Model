import pickle
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score

from src.data_preprocessing import load_and_preprocess_data
from src.utils import get_model_path

def train():
    print("Loading data for classification...")
    X, _, y_clf = load_and_preprocess_data()
    
    X_train, X_test, y_class_train, y_class_test = train_test_split(
        X, y_clf, train_size=0.8, random_state=42
    )

    print("Training Classifier with GridSearch...")
    param_grid_clf = {
        'n_estimators': [50, 100, 200],
        'max_depth': [2, 3, 5],
        'min_samples_split': [10, 15, 20],
        'min_samples_leaf': [5, 10, 20]
    }
    
    gs_clf = GridSearchCV(RandomForestClassifier(class_weight='balanced', random_state=42), 
                          param_grid_clf, cv=3, scoring='accuracy', n_jobs=-1)
    gs_clf.fit(X_train, y_class_train)
    rf_classifier = gs_clf.best_estimator_

    # Evaluation
    y_class_pred = rf_classifier.predict(X_test)
    y_class_prob = rf_classifier.predict_proba(X_test)[:, 1]
    
    print("\n--- Classifier Results ---")
    print(f"Accuracy: {accuracy_score(y_class_test, y_class_pred):.2f}")
    print(f"ROC AUC : {roc_auc_score(y_class_test, y_class_prob):.2f}")
    print(f"Best Params: {gs_clf.best_params_}")

    # Save
    out_path = get_model_path('classifier_model')
    with open(out_path, "wb") as f:
        pickle.dump(rf_classifier, f)
    print(f"Model successfully saved to {out_path}\n")

if __name__ == "__main__":
    train()
