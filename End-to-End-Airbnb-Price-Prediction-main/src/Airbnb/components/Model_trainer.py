import os
import sys
import numpy as np
import pandas as pd
from dataclasses import dataclass
from src.Airbnb.logger import logging
from catboost import CatBoostRegressor
from src.Airbnb.utils.utils import save_object
from src.Airbnb.exception import customexception
from src.Airbnb.utils.utils import evaluate_model
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

@dataclass 
class ModelTrainerConfig:
    trained_model_file_path = os.path.join('Artifacts', 'Model.pkl')
    lr_model_file_path = os.path.join('Artifacts', 'LR_Model.pkl')
    xgb_model_file_path = os.path.join('Artifacts', 'XGB_Model.pkl')
    
class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
    
    def initate_model_training(self, train_array, test_array):
        try:
            logging.info('Splitting Dependent and Independent variables from train and test data')
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1]
            )

            # High-performance regressors
            models = {
                'LinearRegression': LinearRegression(),
                'CatBoostRegressor': CatBoostRegressor(iterations=600, learning_rate=0.08, depth=6, verbose=0, random_seed=42)
            }
            
            model_report: dict = evaluate_model(X_train, y_train, X_test, y_test, models)
            print("Model Report (R2 Scores):", model_report)
            logging.info(f'Model Report : {model_report}')

            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            
            best_model = models[best_model_name]
            print(f'Best Model Found: {best_model_name} with R2 Score: {best_model_score:.4f}')

            # Save primary best model (CatBoost) and LR
            save_object(file_path=self.model_trainer_config.trained_model_file_path, obj=best_model)
            save_object(file_path=self.model_trainer_config.lr_model_file_path, obj=models['LinearRegression'])
            save_object(file_path=self.model_trainer_config.xgb_model_file_path, obj=best_model)
            
            return best_model_score
        except Exception as e:
            logging.info('Exception occurred at Model Training')
            raise customexception(e, sys)
