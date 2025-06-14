## Common Functions for the project that are used in multiple files
import os
import sys

import numpy as np
import pandas as pd
import dill

from sklearn.metrics import r2_score

from src.exception import CustomException
from src.logger import logging

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)  # Create directory if it doesn't exist

        with open(file_path, 'wb') as file_obj:
            dill.dump(obj, file_obj)
        
    except Exception as e:
        raise CustomException(e, sys)
    
def load_object(file_path):
    try:
        with open(file_path, 'rb') as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys)

def evaluate_model(X_train, y_train, X_test, y_test, models,param):
    """
    Evaluate the performance of different regression models and return a report.
    """
    report = {}
    logging.info("Evaluating models...")
    for model_name, model in models.items():
        try:
            
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            r2_square = r2_score(y_test, y_pred)
            report[model_name] = r2_square
        except Exception as e:
            report[model_name] = str(e)

    logging.info("Model evaluation complete.")
    return report