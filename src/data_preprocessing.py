import pandas as pd
import numpy as np
from src.utils import get_data_path

def load_and_preprocess_data():
    """Loads dataset and preprocesses features and target variables."""
    try:
        df = pd.read_csv(get_data_path())
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find dataset at {get_data_path()}.")
    
    # Target Transformation
    df['log1p_area'] = np.log1p(df['area'])
    
    # Outlier Removal
    threshold = df['area'].quantile(0.99)
    df = df[df['area'] <= threshold]
    
    # Feature Extraction
    features_to_drop = ['area', 'log_area', 'log1p_area', 'fire_occurred', 'oxygen']
    X = df.drop(columns=features_to_drop, errors='ignore')
    
    y_reg = df['log1p_area']
    y_clf = df['fire_occurred']
    
    return X, y_reg, y_clf
