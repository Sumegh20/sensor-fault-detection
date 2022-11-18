
from sensor.exception import SensorException
import sys, os
from sensor.constant.training_pipeline import SAVE_MODEL_DIR, MODEL_TRAINER_DIR_NAME, MODEL_TRAINER_TRAINED_MODEL_DIR, MODEL_TRAINER_TRAINED_MODEL_NAME

class TargetValueMapping:
    def __init__(self):
        self.neg: int = 0
        self.pos: int = 1

    def to_dict(self):
        return self.__dict__

    def reverse_mapping(self):
        mapping_response = self.to_dict()
        return dict(zip(mapping_response.values(), mapping_response.keys()))


#Write a code to train model and check the accuracy.

class SensorModel:

    def __init__(self,preprocessor,model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise SensorException(e, sys)

    def predict(self,x):
        try:
            x_transform = self.preprocessor.transform(x)
            y_hat = self.model.predict(x_transform)
            
            return y_hat
        except Exception as e:
            raise SensorException(e, sys)

    def get_best_model():
        pass


class ModelResolver:

    def __init__(self, model_dir=SAVE_MODEL_DIR):
        try:
            self.model_dir = model_dir

        except Exception as e:
            raise SensorException(e, sys)

    def get_best_model_path(self):
        try:
            timestamps = list(map(int, os.listdir(self.model_dir)))
            latest_timestamps = max(timestamps)
            latest_model_path = os.path.join(self.model_dir, f"{latest_timestamps}", MODEL_TRAINER_TRAINED_MODEL_NAME)

            return latest_model_path
        except Exception as e:
            raise SensorException(e, sys)

    def is_model_exists(self)->bool:
        try:
            if not os.path.exists(self.model_dir):
                return False

            timestamps = os.listdir(self.model_dir)
            if len(timestamps) == 0:
                return False

            latest_model_path = self.get_best_model_path()
            if not os.path.exists(latest_model_path):
                return False

            return True
        except Exception as e:
            raise SensorException(e, sys)
