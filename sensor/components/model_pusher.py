from sensor.entity.artifact_entity import DataValidationArtifact, ModelTrainerArtifact, ModelEvaluationArtifact, ModelPusherArtifact
from sensor.entity.config_entity import ModelEvaluationConfig, ModelPusherConfig
from sensor.exception import SensorException
from sensor.logger import logging
#from sensor.ml.metric import calculate_metric
from sensor.ml.metric.classification_metric import get_classification_score
from sensor.ml.model.estimator import SensorModel
from sensor.utils.main_utils import load_object, save_object, write_yaml_file
import sys, os
from sensor.ml.model.estimator import ModelResolver
from sensor.constant.training_pipeline import TARGET_COLUMN
import shutil


class ModelPusher:
    def __init__(self, model_evel_artifact:ModelEvaluationArtifact, model_pusher_config:ModelPusherConfig):
        try:
            self.model_evel_artifact = model_evel_artifact
            self.model_pusher_config = model_pusher_config
        except Exception as e:
            raise SensorException(e, sys)

    def initiate_model_pusher(self,) -> ModelPusherArtifact:
        try:
            trained_model_path = self.model_evel_artifact.trained_model_path
            
            #create model pusher dir to save model
            model_file_path = self.model_pusher_config.model_file_path
            os.makedirs(os.path.dirname(model_file_path), exist_ok=True)
            shutil.copy(src=trained_model_path, dst=model_file_path)

            #saved model dir
            save_model_path = self.model_pusher_config.save_model_path
            os.makedirs(os.path.dirname(save_model_path), exist_ok=True)
            shutil.copy(src=trained_model_path, dst=save_model_path)

            # Creating model pusher artifact
            model_pusher_artifact = ModelPusherArtifact(save_model_path=save_model_path, model_path=model_file_path)
            return model_pusher_artifact
        except Exception as e:
            raise SensorException(e, sys)

