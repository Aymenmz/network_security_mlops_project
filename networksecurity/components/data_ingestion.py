import os
import json
import sys
import numpy as np
import pymongo
import pandas as pd
from typing import List
from dotenv import load_dotenv

from sklearn.model_selection import train_test_split
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_URI")



class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def export_data_from_mongodb(self) -> pd.DataFrame:
        try:
            client = pymongo.MongoClient(MONGO_DB_URL)
            db = client[self.data_ingestion_config.database_name]
            collection = db[self.data_ingestion_config.collection_name]
            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"])
            df.replace({"na": np.nan}, inplace=True)
            logging.info(df[:5])
            logging.info(f"Exported {len(df)} records from MongoDB collection {self.data_ingestion_config.collection_name}")
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def export_data_to_feature_store(self, df: pd.DataFrame):

        feature_store_path = self.data_ingestion_config.feature_store_dir

        os.makedirs(os.path.dirname(feature_store_path), exist_ok=True)

        df.to_csv(feature_store_path, index=False)

        logging.info(f"Data exported to feature store at {feature_store_path}")

        return df
    
    def split_data_as_train_test(self, df: pd.DataFrame):
        try:
            train_set, test_set = train_test_split(
                df,
                test_size=self.data_ingestion_config.train_test_split_ratio,
                random_state=42
            )
            os.makedirs(os.path.dirname(self.data_ingestion_config.training_file_dir), exist_ok=True)
            train_set.to_csv(self.data_ingestion_config.training_file_dir, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_dir, index=False, header=True)
            logging.info(f"Data split into train and test sets with ratio {self.data_ingestion_config.train_test_split_ratio}")
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def initiate_data_ingestion(self):
        try:
            df = self.export_data_from_mongodb()
            df = self.export_data_to_feature_store(df)
            self.split_data_as_train_test(df)
            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_dir,
                testing_file_path=self.data_ingestion_config.testing_file_dir
            )
            return data_ingestion_artifact
            logging.info(f"Data ingested successfully to {self.data_ingestion_config.feature_store_dir}")   
        except Exception as e:
            raise NetworkSecurityException(e, sys)