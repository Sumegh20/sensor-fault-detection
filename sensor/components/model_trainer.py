from sensor.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from sensor.entity.config_entity import ModelTrainerConfig
from sensor.exception import SensorException
from sensor.logger import logging
#from sensor.ml.metric import calculate_metric
from sensor.ml.metric.classification_metric import get_classification_score
from sensor.ml.model.estimator import SensorModel
from sensor.utils.main_utils import load_numpy_array_data, load_object, save_object
import sys, os
from xgboost import XGBClassifier



class ModelTrainer:
    def __init__(self, data_transformation_artifact: DataTransformationArtifact, model_trainer_config: ModelTrainerConfig):
        try:
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_config = model_trainer_config
        except Exception as e:
            raise SensorException(e, sys)

    def train_model(self, x_train, y_train):
        try:
            xgb_clf = XGBClassifier()
            xgb_clf.fit(x_train, y_train)

            return xgb_clf
        except Exception as e:
            raise SensorException(e, sys)

    def initiate_model_trainer(self,) -> ModelTrainerArtifact:
        logging.info("Entered initiate_model_trainer method of ModelTrainer class")

        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            train_arr = load_numpy_array_data(file_path = train_file_path)
            test_arr = load_numpy_array_data(file_path = test_file_path)

            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )

            model = self.train_model(x_train=x_train, y_train=y_train)
            y_train_pred = model.predict(x_train)
            classifictaion_train_matric = get_classification_score(y_true=y_train, y_pred=y_train_pred)
            
            #Underfitting
            # if classifictaion_train_matric.f1_score <= self.model_trainer_config.expected_accuracy:
            #     raise Exception("Model is not good. It is Underfited.")

            y_test_pred = model.predict(x_test)
            classifictaion_test_matric = get_classification_score(y_true=y_test, y_pred=y_test_pred)

            #Overfitting
            # f1_score_diff = abs(classifictaion_train_matric.f1_score - classifictaion_test_matric.f1_score)
            # if f1_score_diff < self.model_trainer_config.overfitting_threshold:
            #     raise Exception("Model is not good. It is Overfited.")

            preprocessor_obj = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
            sensor_model = SensorModel(preprocessor = preprocessor_obj, model = model)

            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path, exist_ok=True)
            save_object(self.model_trainer_config.trained_model_file_path, obj=sensor_model)

            model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                                train_metric_artifact=classifictaion_train_matric,
                                test_metric_artifact=classifictaion_test_matric)

            logging.info(f"Model trainer artifact: {model_trainer_artifact}")

            return model_trainer_artifact
            
            # model_factory = ModelFactory(model_config_path=self.model_trainer_config.model_config_file_path)

            # best_model_detail = model_factory.get_best_model(
            #     X=x_train,
            #     y=y_train,
            #     base_accuracy=self.model_trainer_config.expected_accuracy,
            # )

            # preprocessing_obj = load_object(
            #     file_path=self.data_transformation_artifact.transformed_object_file_path
            # )

            # if (
            #     best_model_detail.best_score
            #     < self.model_trainer_config.expected_accuracy
            # ):
            #     logging.info("No best model found with score more than base score")

            #     raise Exception("No best model found with score more than base score")

            # sensor_model = SensorModel(
            #     preprocessing_object=preprocessing_obj,
            #     trained_model_object=best_model_detail.best_model,
            # )

            # logging.info(
            #     "Created Sensor truck model object with preprocessor and model"
            # )

            # logging.info("Created best model file path.")

            # save_object(self.model_trainer_config.trained_model_file_path, sensor_model)

            # metric_artifact = calculate_metric(
            #     model=best_model_detail.best_model, x=x_test, y=y_test
            # )

            # model_trainer_artifact = ModelTrainerArtifact(
            #     trained_model_file_path=self.model_trainer_config.trained_model_file_path,
            #     metric_artifact=metric_artifact,
            # )

            # logging.info(f"Model trainer artifact: {model_trainer_artifact}")

            # return model_trainer_artifact

        except Exception as e:
            raise SensorException(e, sys) from e
