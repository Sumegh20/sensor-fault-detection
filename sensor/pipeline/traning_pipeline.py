from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig, DataTransformationConfig
from sensor.entity.config_entity import ModelTrainerConfig, ModelEvaluationConfig, ModelPusherConfig
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact
from sensor.entity.artifact_entity import ModelEvaluationArtifact, ModelPusherArtifact, ModelTrainerArtifact
from sensor.exception import SensorException
import sys,os
from sensor.logger import logging
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation
from sensor.components.model_trainer import ModelTrainer
from sensor.components.model_evaluation import ModelEvaluation
from sensor.components.model_pusher import ModelPusher

class TrainPipeline:

    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        
    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Starting data ingestion")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"Data ingestion completed and artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except  Exception as e:
            raise  SensorException(e,sys)

    def start_data_validaton(self,data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        try:
            data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
            data_validation_config = data_validation_config
            )
            data_validation_artifact = data_validation.initiate_data_validation()
            return data_validation_artifact
        except  Exception as e:
            raise  SensorException(e,sys)

    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact):
        try:
            data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,
            data_transformation_config=data_transformation_config
            )
            data_transformation_artifact =  data_transformation.initiate_data_transformation()
            return data_transformation_artifact
        except  Exception as e:
            raise  SensorException(e,sys)
    
    def start_model_trainer(self, data_transformation_artifact:DataTransformationArtifact):
        try:
            model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            model_trainer = ModelTrainer(model_trainer_config=model_trainer_config, data_transformation_artifact = data_transformation_artifact)
            model_artifact = model_trainer.initiate_model_trainer()
            return model_artifact
        except  Exception as e:
            raise  SensorException(e,sys)

    def start_model_evaluation(self, data_validation_artifact: DataValidationArtifact, model_trainer_artifact: ModelTrainerArtifact):
        try:
            model_evel_config = ModelEvaluationConfig(self.training_pipeline_config)
            model_evel = ModelEvaluation(model_eval_config=model_evel_config, data_validation_artifact=data_validation_artifact, model_trainer_artifact=model_trainer_artifact)
            model_evel_artifact = model_evel.initiate_model_evaluation()

            return model_evel_artifact
        except  Exception as e:
            raise  SensorException(e,sys)

    def start_model_pusher(self, model_evel_artifact:ModelEvaluationArtifact):
        try:
            model_pusher_config = ModelPusherConfig(training_pipeline_config=self.training_pipeline_config)
            model_pusher = ModelPusher(model_pusher_config = model_pusher_config, model_evel_artifact = model_evel_artifact)
            model_pusher_artifact = model_pusher.initiate_model_pusher()

            return model_pusher_artifact
        except  Exception as e:
            raise  SensorException(e,sys)

    def run_pipeline(self):
        try:
            data_ingestion_artifact:DataIngestionArtifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validaton(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact = data_transformation_artifact)
            model_evel_artifact = self.start_model_evaluation(data_validation_artifact = data_validation_artifact, model_trainer_artifact = model_trainer_artifact)

            if not model_evel_artifact.is_model_accepted:
                print("Trained model is not better then the best model")
            else:
                model_pusher_artifact = self.start_model_pusher(model_evel_artifact = model_evel_artifact)
        except  Exception as e:
            raise  SensorException(e,sys)