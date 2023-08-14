
import os, sys

from multiplicationTable.entity import config_entity
from multiplicationTable.components.data_ingestion import DataIngestion
from multiplicationTable.components.data_validation import DataValidation
from multiplicationTable.components.data_transformation import DataTransformation
from multiplicationTable.exception import MultiplicationException



try:
    training_pipeline_config = config_entity.TrainingPipelineConfig()

    #data ingestion         
    data_ingestion_config  = config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
    print(data_ingestion_config.to_dict())
    data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
    data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

    #data validation
    data_validation_config = config_entity.DataValidationConfig(training_pipeline_config=training_pipeline_config)
    data_validation = DataValidation(data_validation_config=data_validation_config,
                data_ingestion_artifact=data_ingestion_artifact)
    data_validation_artifact = data_validation.initiate_data_validation()

    #data transformation
    data_transformation_config = config_entity.DataTransformationConfig(training_pipeline_config=training_pipeline_config)
    data_transformation = DataTransformation(data_transformation_config=data_transformation_config, 
    data_validation_artifact=data_validation_artifact)
    data_transformation_artifact = data_transformation.initiate_data_transformation()

except Exception as e:
    raise MultiplicationException(error_message=e, error_detail=sys)