## Code related to data transformation

import sys
import os
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

# This config class is used to store important settings or paths needed during the data transformation process.
# Right now, it holds the file path where we will save the preprocessor object (a trained pipeline that handles
# missing values, encoding, and scaling). At the beginning, this path is just stored as a value – nothing is saved yet.
# But after we train the preprocessor using the training data, we save it to this path using this config.
# Later, when we need to use the same preprocessor (e.g., during model prediction), we can load it back from this path.
# This helps keep our code clean and organized, because instead of hardcoding file paths in multiple places,
# we define them in one place (config class), which makes the code easier to manage, especially in bigger projects.

@dataclass
class DataTransformationConfig:
    """Configuration class for data transformation."""
    preprocessor_obj_file_path: str = os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    """Main class to perform data transformation.
    Responsible for data transformation tasks such as scaling and encoding features.
    It uses a configuration class to manage file paths and settings.
    """
    
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()  # Load configuration

    def get_data_transformer_object(self):
        """Creates a preprocessor object for transforming the data."""
        
        try:
            logging.info("Data Transformation initiated")
            ## Define numerical and categorical features
            numerical_features = ['writing_score', 'reading_score']
            categorical_features = [
                'gender',
                'race_ethnicity',
                'parental_level_of_education',
                'lunch',
                'test_preparation_course'
            ]
            logging.info("Numerical and categorical features identified")

            ## Create a pipeline for numerical features
            num_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='median')),  # Handle missing values
                ('scaler', StandardScaler())  # Scale numerical features
            ])

            ## Create a pipeline for categorical features
            cat_pipeline =  Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),  # Handle missing values
                ('onehot', OneHotEncoder(handle_unknown='ignore')) , # Encode categorical features
                ('scaler', StandardScaler(with_mean=False))  # Scale categorical features
            ])
            logging.info("Pipelines for numerical and categorical features created")
            ## Combine both pipelines into a ColumnTransformer
            preprocessor = ColumnTransformer(
                transformers=[
                    ('num', num_pipeline, numerical_features),
                    ('cat', cat_pipeline, categorical_features)
                ]
            )

            logging.info("ColumnTransformer created with numerical and categorical pipelines")
            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)  # Handle any errors 
    
    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df= pd.read_csv(train_path)
            test_df= pd.read_csv(test_path)
            logging.info("Read train and test data successfully for transformation")
            logging.info("Obtaining preprocessor object")
            preprocessor_obj = self.get_data_transformer_object()

            target_column_name = 'math_score'
            numerical_columns = ['writing_score', 'reading_score']

            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info("Applying preprocessor on training and testing dataframes")

            input_feature_train_arr = preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessor_obj.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
            logging.info("Data transformation completed successfully")
            
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessor_obj
            )
            return (
                train_arr,
                test_arr, 
                #self.data_transformation_config.preprocessor_obj_file_path,
            )
        except Exception as e:
            raise CustomException(e, sys) 