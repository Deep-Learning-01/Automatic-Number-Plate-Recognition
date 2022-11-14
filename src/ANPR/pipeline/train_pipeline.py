import os,sys
from src.ANPR.components.data_ingestion import DataIngestion
from src.ANPR.components.data_transformation import DataTransformation
from src.ANPR.entity.config_entity import DataIngestionConfig, DataTransformationConfig

from src.ANPR.entity.artifacts_entity import DataIngestionArtifacts, DataTransformationArtifacts
from src.ANPR.config.s3_opearations import S3Operation
from src.ANPR.logger import logging
from src.ANPR.exception import ANPRException

class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.s3_operations = S3Operation()
    
    def start_data_ingestion(self)-> DataIngestionArtifacts:
        logging.info("Entered the start_data_ingestion method of TrainPipeline class")
        try:
            logging.info("Getting the compressed data from S3 Bucket")
            data_injestion_obj  = DataIngestion(data_ingestion_config = self.data_ingestion_config, S3_operations=S3Operation())
            data_ingestion_artifact = data_injestion_obj.initiate_data_ingestion()
            logging.info("Got the extracted data ")
            return data_ingestion_artifact
        except Exception as e:
            raise ANPRException(e,sys) from e

    def start_data_transformation(self, data_ingestion_artifact: DataIngestionArtifacts) -> DataTransformationArtifacts:
        logging.info("Entered the start_data_transformation method of TrainPipeline class")
        try:
            data_transformation = DataTransformation(data_ingestion_artifact=data_ingestion_artifact,data_transformation_config=self.data_transformation_config)
            data_transformation.initiate_data_transformation()
        except Exception as e:
            raise ANPRException(e,sys) from e
    
    def run_pipeline(self) -> None:
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            self.start_data_transformation(data_ingestion_artifact=data_ingestion_artifact)
        except Exception as e:
            raise ANPRException(e,sys) from e