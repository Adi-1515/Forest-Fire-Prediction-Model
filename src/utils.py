import os

def get_project_root():
    """Returns absolute path to the project root directory."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_data_path():
    return os.path.join(get_project_root(), "data", "dataset.csv")

def get_model_path(model_name):
    return os.path.join(get_project_root(), "models", f"{model_name}.pkl")
