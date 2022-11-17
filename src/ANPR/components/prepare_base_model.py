import os, sys
from src.ANPR.entity.config_entity import PrepareBaseModelConfig
from src.ANPR.entity.artifacts_entity import PrepareBaseModelArtifacts
from src.ANPR.logger import logging
from src.ANPR.exception import ANPRException
from src.ANPR.constants import *
from src.ANPR.utils.utils import *
from pathlib import Path
import tensorflow as tf

class PrepareBaseModel:
    def __init__(self, prepare_base_model_config : PrepareBaseModelConfig) :
        self.prepare_base_model_config = prepare_base_model_config

    def get_base_model(self):
        """
        Method Name :   get_base_model
        Description :   This method will  use the Inception-ResNet-v2 model with pre-trained weights and save it as base model.
        """
        self.model = tf.keras.applications.InceptionResNetV2(
            input_shape= IMAGE_SIZE,
            weights= WEIGHTS,
            include_top= INCLUDE_TOP
        )
        base_model_path = Path(self.prepare_base_model_config.BASEMODEL_PATH)
        self.save_model(path=base_model_path,model=self.model)

    def _prepare_full_model(self,model,classes,freeze_all,freeze_till, learning_rate):
        """
        Method Name :   _prepare_full_model
        Description :   This hidden method will compile the model and produce our summary and save it as updated model
        """ 
        if freeze_all:
            for layer in model.layers:
                layer.trainable = False
        elif (freeze_till is not None) and (freeze_till > 0 ):
            for layer in model.layers[:-freeze_till]:
                layer.trainable = False
        flatten_in = tf.keras.layers.Flatten()(model.output)
        prediction = tf.keras.layers.Dense(
            units= classes,
            activation='softmax'
        )(flatten_in)
        final_model = tf.keras.models.Model(
            inputs = model.input,
            outputs = prediction
        )
        final_model.compile(
            optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate),
            metrics = ['accuracy'],
            loss='mse'
        )
        print(final_model.summary())
        return final_model

    def get_updated_model(self):
        self.final_model = self._prepare_full_model(
            model = self.model,
            classes = CLASSES,
            freeze_all = FREEZE_ALL,
            freeze_till = None,
            learning_rate = LEARNING_RATE
        )
        self.save_model(path = self.prepare_base_model_config.UPDATED_MODEL_PATH,model = self.final_model)

    @staticmethod
    def save_model(path : Path, model : tf.keras.Model):
        model.save(path)
        
    
    def initiate_prepare_basemodel(self):
        try: 
            logging.info("Entered the initiate_prepare_basemodel method of PrepareBaseModel class")

            os.makedirs(self.prepare_base_model_config.PREPARE_BASEMODEL_ARTIFACTS_DIR,exist_ok=True)

            self.get_base_model()

            self.get_updated_model()

            prepare_base_model_artifact = PrepareBaseModelArtifacts(
                base_model_file_path=self.prepare_base_model_config.BASEMODEL_PATH,
                updated_model_filr_path= self.prepare_base_model_config.UPDATED_MODEL_PATH
            )
            logging.info("Exited the initiate_prepare_basemodel method of PrepareBaseModel class")

            return prepare_base_model_artifact

        except Exception as e:
            raise ANPRException(e, sys) from e
    