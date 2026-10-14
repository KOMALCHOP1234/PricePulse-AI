import os
import sys
import pandas as pd
from src.Airbnb.logger import logging
from src.Airbnb.exception import customexception
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    raw_data_path: str = os.path.join("Artifacts", "raw_data.csv")
    train_data_path: str = os.path.join("Artifacts", "train_data.csv")
    test_data_path: str = os.path.join("Artifacts", "test_data.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("India Data ingestion started")
        try:
            csv_path = os.path.join("Notebook_Experiments", "Data", "Airbnb_India_Data.csv")
            data = pd.read_csv(csv_path)
            logging.info(f"Read Indian Airbnb dataset: {data.shape} rows and columns")

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)
            data.to_csv(self.ingestion_config.raw_data_path, index=False)

            train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)
            train_data.to_csv(self.ingestion_config.train_data_path, index=False)
            test_data.to_csv(self.ingestion_config.test_data_path, index=False)
            logging.info("Splitting into Indian train and test data completed")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            logging.info("Exception occurred while ingesting the India data")
            raise customexception(e, sys)