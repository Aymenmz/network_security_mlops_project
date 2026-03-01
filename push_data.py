import os
import json
import sys
from dotenv import load_dotenv
import certifi
import pymongo
import pandas as pd
import numpy as np
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging



load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_URI")

ca = certifi.where()


class NetworkDataExtractor:
    def __init__(self, mongo_client):
        try:
            self.mongo_client = mongo_client
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def csv_to_json(self, csv_file_path):
        try:
            df = pd.read_csv(csv_file_path)
            df.reset_index(drop=True, inplace=True)
            return df.to_dict(orient='records')
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def insert_data_mongodb(self, data, database_name, collection_name):
        try:
            db = self.mongo_client[database_name]
            collection = db[collection_name]
            collection.insert_many(data)

            logging.info(
                f"Inserted {len(data)} records into {database_name}.{collection_name}"
            )
        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    try:

        if not MONGO_DB_URL:
            raise NetworkSecurityException("MONGO_URI environment variable is missing or not set.", sys)
        client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
        network_data_extractor = NetworkDataExtractor(mongo_client=client)
        csv_file_path = "/Users/aymen/personal-projects/mlops/networkSecurity/network_data/phisingData.csv"
        DATABASE_NAME = "network_security"
        COLLECTION_NAME = "phishing_data"
        data = network_data_extractor.csv_to_json(csv_file_path)
        network_data_extractor.insert_data_mongodb(
            data, DATABASE_NAME, COLLECTION_NAME
        )
    except Exception as e:
        raise NetworkSecurityException(e, sys)
