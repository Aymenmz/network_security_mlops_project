import os
import sys
import numpy as np
import pandas as pd


"""
    Defining Training Pipeline Constants
"""
TARGET_COLUMN = "Result"
PIPELINE_NAME = "network_security_pipeline"
ARTIFACT_DIR = "artifacts"
FILE_NAME = "phishingData.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"

""" 
    Data Ingestion Constants
"""

DATA_INGESTION_COLLECTION_NAME = "phishing_data"
DATA_INGESTION_DATABASE_NAME = "network_security"
DATA_INGESTION_DIR_NAME = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR = "feature_store"
DATA_INGESTION_INGESTED_DIR = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO = 0.2