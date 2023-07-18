import sys
from dataclasses import dataclass

import numpy as np 
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.exception import CustomException
from src.logger import logging
import os

from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts',"proprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformer_object(self):
        """
        Returns a data transformer object that preprocesses the data for modeling.

        This function initializes and configures two pipelines: `num_pipeline` and `cat_pipeline`. The `num_pipeline` applies the following steps to the numerical columns ["writing_score", "reading_score"]:
        - Imputes missing values using the median strategy
        - Scales the data using StandardScaler

        The `cat_pipeline` applies the following steps to the categorical columns ["gender", "race_ethnicity", "parental_level_of_education", "lunch", "test_preparation_course"]:
        - Imputes missing values using the most frequent strategy
        - Encodes the categorical columns using OneHotEncoder
        - Scales the data using StandardScaler with mean=False

        The function then creates a `preprocessor` object using ColumnTransformer. The `preprocessor` applies the `num_pipeline` to the numerical columns and the `cat_pipeline` to the categorical columns.

        Returns:
        - preprocessor: A ColumnTransformer object that preprocesses the data for modeling.

        Raises:
        - CustomException: If an error occurs during the execution of the function.
        """
        try:
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            num_pipeline= Pipeline(
                steps=[
                ("imputer",SimpleImputer(strategy="median")),
                ("scaler",StandardScaler())

                ]
            )

            cat_pipeline=Pipeline(

                steps=[
                ("imputer",SimpleImputer(strategy="most_frequent")),
                ("one_hot_encoder",OneHotEncoder()),
                ("scaler",StandardScaler(with_mean=False))
                ]

            )

            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            preprocessor=ColumnTransformer(
                [
                ("num_pipeline",num_pipeline,numerical_columns),
                ("cat_pipelines",cat_pipeline,categorical_columns)

                ]


            )

            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,train_path,test_path):
        """
        Initiates the data transformation process.

        Args:
            train_path (str): The file path to the training data.
            test_path (str): The file path to the testing data.

        Returns:
            tuple: A tuple containing:
                - train_arr (numpy.ndarray): The transformed training data array.
                - test_arr (numpy.ndarray): The transformed testing data array.
                - preprocessor_obj_file_path (str): The file path to the saved preprocessing object.
        Raises:
            CustomException: If an exception occurs during the data transformation process.
        """
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("Read train and test data completed")

            logging.info("Obtaining preprocessing object")

            preprocessing_obj=self.get_data_transformer_object()

            target_column_name="math_score"
            numerical_columns = ["writing_score", "reading_score"]

            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]

            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info(f"Saved preprocessing object.")

            save_object(

                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj

            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
        except Exception as e:
            raise CustomException(e,sys)

