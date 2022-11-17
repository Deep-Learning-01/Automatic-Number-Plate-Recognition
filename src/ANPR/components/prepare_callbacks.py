import os, sys, time
from src.ANPR.entity.config_entity import *
from src.ANPR.entity.artifacts_entity import *
from src.ANPR.logger import logging
from src.ANPR.exception import ANPRException
from src.ANPR.constants import *
from src.ANPR.utils.utils import *
from pathlib import Path
import tensorflow as tf

class PrepareCallbacks:
    def __init__(self,prepare_callbacks_config:PrepareCallbacksConfig) -> None:
        self.prepare_callbacks_config = prepare_callbacks_config

    @property
    def _create_tb_callbacks(self):
        timestamp = time.strftime("%Y-%m-%d-%H-%M-%S")
        tb_running_log_dir = os.path.join(self.prepare_callbacks_config.TENSORBOARD_ROOT_LOG_DIR,f"tb_logs_at_{timestamp}") 
        return tf.keras.callbacks.TensorBoard(log_dir=tb_running_log_dir)

    @property
    def _create_ckpt_callbacks(self):
        return  tf.keras.callbacks.ModelCheckpoint(
            filepath=self.prepare_callbacks_config.CHECKPOINT_MODEL_FILEPATH,
            save_best_only=True
        )

    def get_tensorboard_checkpoint_callbacks(self):
        return [
            self._create_tb_callbacks,
            self._create_ckpt_callbacks
        ]

    def initiate_prepare_callbacks(self):
        try: 
            logging.info("Entered the initiate_prepare_callbacks method of PrepareCallbacks class")

            model_ckpt_dir = os.path.dirname(self.prepare_callbacks_config.CHECKPOINT_MODEL_FILEPATH)

            create_directories([model_ckpt_dir, self.prepare_callbacks_config.TENSORBOARD_ROOT_LOG_DIR])

            prepare_callbacks_artifact = PrepareCallbacksArtifacts(callback_list=self.get_tensorboard_checkpoint_callbacks())

            logging.info("Exited the initiate_prepare_callbacks method of PrepareCallbacks class")

            return prepare_callbacks_artifact

        except Exception as e:
            raise ANPRException(e, sys) from e