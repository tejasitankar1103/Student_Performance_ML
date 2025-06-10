## It will contain code to handle data ingestion from various sources.

import os
import sys
from src.exception import CustomException
from src.logger import logging

import pandas as pd

from src.components.data_transformation import DataTransformationConfig
from src.components.data_transformation import DataTransformation

from sklearn.model_selection import train_test_split
from dataclasses import dataclass # For simple configuration class

## Configuration class for storing file paths for raw, train, and test data
@dataclass ##decorator to automatically generate special methods like __init__ and __repr__
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', 'train.csv')
    test_data_path: str = os.path.join('artifacts', 'test.csv')
    raw_data_path: str = os.path.join('artifacts', 'data.csv')

## Main class to perform data ingestion
## not using @dataclass here because we want to define methods in this class
class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()  # Load file paths

    def initiate_data_ingestion(self):
        logging.info("Data Ingestion Method Started")
        try:
            # Step 1: Read the CSV file containing the data
            df = pd.read_csv('notebook/data/stud.csv')
            logging.info('Read the dataset as dataframe')

            # Step 2: Create the folder for saving files, if it doesn't already exist
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            # Step 3: Save the raw data for backup
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            # Step 4: Split the data into train and test (80-20 split)
            logging.info('Train test split initiated')
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            # Step 5: Save the train and test datasets
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info('Ingestion of data is completed')

            # Step 6: Return file paths for further processing
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
                self.ingestion_config.raw_data_path
            )

        except Exception as e:
            raise CustomException(e, sys)  # Handle any errors

# If this file is run directly, start the ingestion process
if __name__ == "__main__":
    obj = DataIngestion()
    train_data,test_data,_ = obj.initiate_data_ingestion()
    print("Data Ingestion Completed")

    data_transformation = DataTransformation()
    data_transformation.initiate_data_transformation(train_data, test_data)
