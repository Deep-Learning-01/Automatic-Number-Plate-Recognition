import os
from datetime import datetime
from from_root import from_root

from pathlib import Path

CONFIG_FILE_PATH = Path("configs/config.yaml")
PARAMS_FILE_PATH = Path("params.yaml")

TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

# Data Ingestion related constants
ARTIFACTS_DIR = os.path.join(from_root(), "artifacts")
BUCKET_NAME = 'anpr-io-files'
S3_DATA_FOLDER_NAME = "images.zip"
DATA_INGESTION_ARTIFACTS_DIR = "DataIngestion"
UNZIP_FOLDER_NAME = 'images/'

# Data Transformation related constants
DATA_TRANSFORMATION_ARTIFACTS_DIR = "DataTransformation"
LABELED_DATAFRAME = "labels.csv"
TRANSFORMED_DATA='data.npy'
TRANSFORMED_OUTPUT='output.npy'

# Prepare Base Model related constants
PREPARE_BASE_MODEL_DIR = "PrepareBaseModel"
BASE_MODEL_PATH = 'base_model.h5'
UPDATED_MODEL_PATH = 'updated_model.h5'
AUGMENTAION = True
IMAGE_SIZE = [224,224,3] # As per InceptionResNetV2
BATCH_SIZE = 16
INCLUDE_TOP = False
EPOCHS= 180
WEIGHTS = 'imagenet'
LEARNING_RATE = 1e-4
CLASSES = 4
FREEZE_ALL= True