from sensor.exception import SensorException
import sys, os
from sensor.logger import logging
from sensor.pipeline import traning_pipeline
from sensor.pipeline.traning_pipeline import TrainPipeline

#from sensor.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig

if __name__ == "__main__":
    try:
        traning_pipeline = TrainPipeline()
        traning_pipeline.run_pipeline()
    except Exception as e:
        print(e)
        logging.exception(e)