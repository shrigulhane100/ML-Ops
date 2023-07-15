import os
import sys
from src.exception import CustumeException
from src.logger import logging

import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    train_data_path: str=os.path.join('artifacts',"train.csv")
    test_data_path: str=os.path.join('artifacts',"test.csv")
    raw_data_path: str=os.path.join('artifacts',"data.csv")


class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()

    def intiate_data_ingestion(self):
        """
        Initiates the data ingestion process.

        Reads a CSV file as a DataFrame, saves it to the raw data path,
        performs a train-test split, and saves the train and test datasets
        to their respective paths.

        Returns:
            Tuple[str, str]: A tuple containing the paths to the train and test datasets.

        Raises:
            CustumeException: If an error occurs during the data ingestion process.
        """
        logging.info("Entered the data ingestion method or component")
        try:
            df=pd.read_csv('notebook\data\stud.csv')
            logging.info("Read dataset as DataFrame successfully")

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path,exist_ok=True), exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path,index=False, header=True)
            logging.info("Train-Test split intiated successfully.")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            logging.info("Data ingestion completed successfully")

            return(self.ingestion_config.train_data_path,
                   self.ingestion_config.test_data_path)

        except Exception as e:
            raise CustumeException(e, sys)
        

if __name__=="__main__":
    obj=DataIngestion()
    obj.intiate_data_ingestion()
