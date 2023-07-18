import os
import sys

import numpy as np 
import pandas as pd
import dill
import pickle
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException

def save_object(file_path, obj):
    """
    Save an object to a file.

    Args:
        file_path (str): The path to the file where the object will be saved.
        obj: The object to be saved.

    Raises:
        CustomException: If there was an exception during the saving process.

    Returns:
        None
    """
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)
    
def evaluate_models(X_train, y_train,X_test,y_test,models,param):
    """
    Evaluate multiple models using grid search and return a dictionary of the model scores.

    Parameters:
    - X_train (array-like): The training data.
    - y_train (array-like): The target variable for the training data.
    - X_test (array-like): The test data.
    - y_test (array-like): The target variable for the test data.
    - models (dict): A dictionary of model names as keys and model instances as values.
    - param (dict): A dictionary of model names as keys and model parameters as values.

    Returns:
    - report (dict): A dictionary containing the model names as keys and the R^2 scores as values.

    Raises:
    - CustomException: If an error occurs during the execution of the function.
    """
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            para=param[list(models.keys())[i]]

            gs = GridSearchCV(model,para,cv=3)
            gs.fit(X_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)

            #model.fit(X_train, y_train)  # Train model

            y_train_pred = model.predict(X_train)

            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)

            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        return report

    except Exception as e:
        raise CustomException(e, sys)
    
def load_object(file_path):
    """
    Load an object from a file.

    Args:
        file_path (str): The path to the file to be loaded.

    Returns:
        The loaded object.

    Raises:
        CustomException: If there is an error loading the object from the file.
    """
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)

    except Exception as e:
        raise CustomException(e, sys)


