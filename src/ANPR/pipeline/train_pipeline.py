import os,sys
from src.ANPR.components.data_ingestion import DataIngestion
from src.ANPR.components.data_transformation import DataTransformation
from src.ANPR.components.prepare_base_model import PrepareBaseModel
from src.ANPR.components.prepare_callbacks import PrepareCallbacks
from src.ANPR.components.model_training import ModelTraining
from src.ANPR.entity.config_entity import *

from src.ANPR.entity.artifacts_entity import *
from src.ANPR.config.s3_opearations import S3Operation
from src.ANPR.logger import logging
from src.ANPR.exception import ANPRException

class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.prepare_base_model_config = PrepareBaseModelConfig()
        self.prepare_callbacks_config = PrepareCallbacksConfig()
        self.training_config = TrainingConfig()
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
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            return data_transformation_artifact
        except Exception as e:
            raise ANPRException(e,sys) from e

    def prepare_base_model(self) -> PrepareBaseModelArtifacts:
        logging.info("Entered the prepare_base_model method of TrainPipeline class")
        try:
            prepare_basemodel_obj = PrepareBaseModel(prepare_base_model_config = self.prepare_base_model_config)
            prepare_base_model_artifact = prepare_basemodel_obj.initiate_prepare_basemodel()
            return prepare_base_model_artifact
            
        except Exception as e:
            raise ANPRException(e,sys) from e
        
    def prepare_callbacks(self):
        logging.info("Entered the prepare_callbacks method of TrainPipeline class")
        try:
            prepare_callback_obj = PrepareCallbacks(prepare_callbacks_config= self.prepare_callbacks_config)
            prepare_callback_obj.initiate_prepare_callbacks()
            
        except Exception as e:
            raise ANPRException(e,sys) from e

    def model_training(self,
         data_ingestion_artifact : DataIngestionArtifacts,
         data_transformation_artifact : DataTransformationArtifacts,
         prepare_base_model_artifact : PrepareBaseModelArtifacts,
    ):
        logging.info("Entered the prepare_callbacks method of TrainPipeline class")
        try:
            training_obj = ModelTraining(
                training_config= self.training_config,
                prepare_callbacks_config= self.prepare_callbacks_config,
                data_ingestion_artifact=data_ingestion_artifact,
                data_transformation_artifact=data_transformation_artifact,
                prepare_base_model_artifact =prepare_base_model_artifact,
                
            )
            training_obj.initiate_model_training()
        except Exception as e:
            raise ANPRException(e,sys) from e

        
    
    def run_pipeline(self) -> None:
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_transformation_artifact = self.start_data_transformation(data_ingestion_artifact=data_ingestion_artifact)
            prepare_base_model_artifact = self.prepare_base_model()
            
            self.model_training(
                data_ingestion_artifact=data_ingestion_artifact,
                data_transformation_artifact=data_transformation_artifact,
                prepare_base_model_artifact =prepare_base_model_artifact
                )
        except Exception as e:
            raise ANPRException(e,sys) from e