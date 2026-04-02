# Forest Fire Prediction System

A production-ready machine learning application designed to predict the likelihood of forest fire occurrences and estimate the potential burned area based on meteorological and environmental conditions. 

> **Important Geographical Limitation:** This model is trained explicitly on the **UCI Forest Fires Dataset**, representing the specific meteorological conditions of the Montesinho Nature Park in the Trás-os-Montes region of northeast Portugal. Predictions reflect localized patterns and **will not reliably generalize** to other global climates, topographies, or regions.

## Project Architecture

This project was built adhering to strict modern software engineering standards, modularizing inference from training and abstracting out UI elements cleanly.

```text
forest-fire-prediction/
│
├── data/
│   └── dataset.csv              # Source UCI Kaggle dataset
├── models/
│   ├── regression_model.pkl     # Persisted Random Forest Regressor
│   └── classifier_model.pkl     # Persisted Random Forest Classifier
├── src/
│   ├── data_preprocessing.py    # Transform target structures and remove outliers
│   ├── train_regression.py      # GridSearch regressor isolated training logic
│   ├── train_classifier.py      # GridSearch classifier isolated training logic
│   ├── predict.py               # Pure headless python inference logic
│   └── utils.py                 # Relative pathing and environment helpers
├── app/
│   └── app.py                   # Streamlit interactive UI application
├── .gitignore                   # Keeps repository clean and restricts model wipes
├── requirements.txt             # Virtual environment dependencies
└── README.md                    # Project documentation
```

## Key Features
*   **Fire Probability Estimation:** Utilizes a Random Forest Classifier to assign a probabilistic likelihood of a fire occurring.
*   **Burned Area Prediction:** Implements a two-stage Random Forest Regressor to safely estimate spread assuming a fire occurs.
*   **Decoupled Architecture:** Inference (`src/predict.py`) is entirely abstracted from the frontend (`app/app.py`), allowing simple drop-in replacement with FastAPI or Flask backends later.

## Tech Stack
*   **Language:** Python 3.8+
*   **Machine Learning:** `scikit-learn`
*   **Data Manipulation:** `pandas`, `numpy`
*   **Frontend UI:** `streamlit`

## Setup & Local Installation

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Adi-1515/forest-fire-prediction.git
    cd forest-fire-prediction
    ```

2.  **Initialize a Virtual Environment:**
    ```bash
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install Required Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage and Model Management

**1. Running the Web Application (Streamlit)**
Since the repository securely stores baseline serialized models, you can instantly boot the user interface without waiting for training blocks:
```bash
streamlit run app/app.py
```

**2. Headless Predictions**
You can invoke the isolated prediction class straight from Python via:
```python
from src.predict import ForestFirePredictor
predictor = ForestFirePredictor()
result = predictor.predict({'X': 5, 'temp': 20.0, ...})
```

**3. Retraining the Models**
If you update the dataset or wish to alter hyperparameter restrictions, models can be cleanly retrained from the root utilizing:
```bash
python src/train_classifier.py
python src/train_regression.py
```

## Dataset Information
Features mapped utilizing the UCI definitions:
*   **Spatial & Temporal:** `X`, `Y` (1-9 mappings), `month`, `day`
*   **FWI (Fire Weather Index) System:** `FFMC`, `DMC`, `DC`, `ISI`
*   **Meteorological Variables:** `temp` (Temperature °C), `RH` (Relative Humidity %), `wind` (Wind speed km/h), `rain` (Outside rain in mm/m²)

## Limitations and Future Improvements
Due to the statistical difficulty of predicting continuous variables based solely on minor meteorological factors, the regression logic natively experiences high variance properties.
Furthermore, biological factors (fuel density) and human factors (intervention response times) heavily dictate exact spread size but are completely absent from this dataset.

**Future Considerations:**
*   Add integration tests bridging the data ingestion to model endpoints.
*   Setup Docker configurations (`Dockerfile`, `docker-compose.yml`) for containerized deployment parity.
*   Integrate model tracking frameworks (like `MLflow`).

## License
See the [LICENSE](LICENSE) file for details.
