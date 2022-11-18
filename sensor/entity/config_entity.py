from datetime import datetime
import os, sys
from sensor.constant  import training_pipeline
from sensor.exception import SensorException

class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        try:
            timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
            self.pipeline_name: str = training_pipeline.PIPELINE_NAME
            self.artifact_dir: str = os.path.join(training_pipeline.ARTIFACT_DIR, timestamp)
            self.timestamp: str = timestamp
        except Exception as e:
            raise SensorException(e, sys)


class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.data_ingestion_dir: str = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.DATA_INGESTION_DIR_NAME)
            self.feature_store_file_path: str = os.path.join(self.data_ingestion_dir, training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR, training_pipeline.FILE_NAME)
            self.training_file_path: str = os.path.join(self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TRAIN_FILE_NAME)
            self.testing_file_path: str = os.path.join(self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TEST_FILE_NAME)
            self.train_test_split_ratio: float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
            self.collection_name: str = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        except Exception as e:
            raise SensorException(e, sys)


class DataValidationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.data_validation_dir: str = os.path.join( training_pipeline_config.artifact_dir, training_pipeline.DATA_VALIDATION_DIR_NAME)
            self.valid_data_dir: str = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_VALID_DIR)
            self.invalid_data_dir: str = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_INVALID_DIR)
            self.valid_train_file_path: str = os.path.join(self.valid_data_dir, training_pipeline.TRAIN_FILE_NAME)
            self.valid_test_file_path: str = os.path.join(self.valid_data_dir, training_pipeline.TEST_FILE_NAME)
            self.invalid_train_file_path: str = os.path.join(self.invalid_data_dir, training_pipeline.TRAIN_FILE_NAME)
            self.invalid_test_file_path: str = os.path.join(self.invalid_data_dir, training_pipeline.TEST_FILE_NAME)
            self.drift_report_file_path: str = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR, training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)
        except Exception as e:
            raise SensorException(e, sys)


class DataTransformationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.data_transformation_dir: str = os.path.join( training_pipeline_config.artifact_dir,training_pipeline.DATA_TRANSFORMATION_DIR_NAME )
            self.transformed_train_file_path: str = os.path.join( self.data_transformation_dir,training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR, training_pipeline.TRAIN_FILE_NAME.replace("csv", "npy"),)
            self.transformed_test_file_path: str = os.path.join(self.data_transformation_dir,  training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR, training_pipeline.TEST_FILE_NAME.replace("csv", "npy"), )
            self.transformed_object_file_path: str = os.path.join( self.data_transformation_dir, training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR, training_pipeline.PREPROCSSING_OBJECT_FILE_NAME,)
        except Exception as e:
            raise SensorException(e, sys)

class ModelTrainerConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.model_trainer_dir: str = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.MODEL_TRAINER_DIR_NAME)
            self.trained_model_file_path: str = os.path.join(self.model_trainer_dir, training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR, training_pipeline.MODEL_FILE_NAME)
            self.expected_accuracy: float = training_pipeline.MODEL_TRAINER_EXPECTED_SCORE
            self.overfitting_threshold:float = training_pipeline.MODEL_TRAINER_OVERFITTING_THRESHOLD
            self.model_config_file_path: str = training_pipeline.MODEL_TRAINER_MODEL_CONFIG_FILE_PATH
        except Exception as e:
            raise SensorException(e, sys)


class ModelEvaluationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.model_evaluation_dir: str = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.MODEL_EVALUATION_DIR_NAME)
            self.changed_threshold_score: float = training_pipeline.MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE
            self.report_file_path: str = os.path.join(self.model_evaluation_dir, training_pipeline.MODEL_EVALUATION_DRIFT_REPORT_FILE_NAME)
        except Exception as e:
            raise SensorException(e, sys)


        # self.bucket_name: str = training_pipeline.MODEL_PUSHER_BUCKET_NAME
        # self.s3_model_key_path: str = os.path.join(training_pipeline.MODEL_PUSHER_S3_KEY, training_pipeline.MODEL_FILE_NAME)

class ModelPusherConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.model_pusher_dir: str = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.MODEL_PUSHER_DIR_NAME)
            self.model_file_path: str = os.path.join(self.model_pusher_dir, training_pipeline.MODEL_FILE_NAME)
            timestamp = datetime.now().strftime("%m%d%Y%H%M%S")
            self.save_model_path: str = os.path.join(training_pipeline.SAVE_MODEL_DIR, timestamp, training_pipeline.MODEL_FILE_NAME)
        except Exception as e:
            raise SensorException(e, sys)