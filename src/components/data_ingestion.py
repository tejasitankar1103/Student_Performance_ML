## It will contain code to handle data ingestion from various sources.

import os
import sys
from src.exception import CustomException
from src.logger import logging

import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

## DataIngestionConfig class to hold the configuration for data ingestion.
## used to specify the paths for raw data, train data, and test data.
## This class will be used to read the data from a CSV file and split it into training and testing sets.
## The class will also handle the creation of directories if they do not exist.
## The class will raise a CustomException if there is an error during the data ingestion process.
## This code is part of a machine learning pipeline that handles data ingestion.

@dataclass ##decorator to automatically generate special methods like __init__ and __repr__
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', 'train.csv')
    test_data_path: str = os.path.join('artifacts', 'test.csv')
    raw_data_path: str = os.path.join('artifacts', 'data.csv')


## not using @dataclass here because we want to define methods in this class
class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Data Ingestion Method Started")
        try:
            df=pd.read_csv('notebook/data/stud.csv')
            logging.info('Read the dataset as dataframe')

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path,index=False, header=True)

            logging.info('Train test split initiated')
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info('Ingestion of data is completed')

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
                self.ingestion_config.raw_data_path
            )

        except Exception as e:
            raise CustomException(e,sys)
        

if __name__ == "__main__":
    obj = DataIngestion()
    obj.initiate_data_ingestion()
    print("Data Ingestion Completed")