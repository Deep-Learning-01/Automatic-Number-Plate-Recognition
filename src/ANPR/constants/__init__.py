import os
from datetime import datetime
from from_root import from_root

from pathlib import Path

CONFIG_FILE_PATH = Path("configs/config.yaml")
PARAMS_FILE_PATH = Path("params.yaml")

TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

ARTIFACTS_DIR = os.path.join(from_root(), "artifacts")
BUCKET_NAME = 'anpr-io-files'
S3_DATA_FOLDER_NAME = "images.zip"
DATA_INGESTION_ARTIFACTS_DIR = "DataIngestion"
UNZIP_FOLDER_NAME = 'images/'

DATA_TRANSFORMATION_ARTIFACTS_DIR = "DataTransformation"
LABELED_DATAFRAME = "labels.csv"
TRANSFORMED_DATA='data.npy'
TRANSFORMED_OUTPUT='output.npy'