from multiplicationTable.entity import artifact_entity,config_entity
from multiplicationTable.exception import MultiplicationException
from multiplicationTable.logger import logging
from typing import Optional
import os,sys 
from sklearn.pipeline import Pipeline
import pandas as pd
from multiplicationTable import utils
import numpy as np
from sklearn.preprocessing import RobustScaler    # To minimize the effect of outliers
from multiplicationTable.config import TARGET_COLUMN


class DataTransformation:

    def __init__(self,data_transformation_config:config_entity.DataTransformationConfig,
                    data_validation_artifact:artifact_entity.DataValidationArtifact):
        try:
            logging.info(f"{'>>'*20} Data Transformation {'<<'*20}")
            self.data_transformation_config=data_transformation_config
            self.data_validation_artifact=data_validation_artifact
        except Exception as e:
            raise MultiplicationException(e, sys)

    @classmethod
    def get_data_transformer_object(cls)->Pipeline:     # Attributes of this class will be same across all the object 
        try:
            robust_scaler =  RobustScaler()
            pipeline = Pipeline(steps=[
                    ('RobustScaler',robust_scaler)  # To handle outliers in one side of distribution
                ])
            return pipeline
        except Exception as e:
            raise MultiplicationException(e, sys)
    

    def initiate_data_transformation(self,) -> artifact_entity.DataTransformationArtifact:
        try:
            # Reading training and testing file
            train_df = pd.read_csv(self.data_validation_artifact.train_file_path)
            test_df = pd.read_csv(self.data_validation_artifact.test_file_path)
            
            # Selecting input feature for train and test dataframe
            input_feature_train_df=train_df.drop(TARGET_COLUMN,axis=1)
            input_feature_test_df=test_df.drop(TARGET_COLUMN,axis=1)

            # Selecting target feature for train and test dataframe
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_test_df = test_df[TARGET_COLUMN]

            transformation_pipleine = DataTransformation.get_data_transformer_object()
            transformation_pipleine.fit(input_feature_train_df)

            # Transforming input features
            input_feature_train_arr = transformation_pipleine.transform(input_feature_train_df)  # Transformaing input features to array
            input_feature_test_arr = transformation_pipleine.transform(input_feature_test_df)
            
            # Target encoder
            train_arr = np.c_[input_feature_train_arr, target_feature_train_df]    # concatenated array
            test_arr = np.c_[input_feature_test_arr, target_feature_test_df]

            # Save numpy array
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_path, array=train_arr)
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_path, array=test_arr)

            # Saving object
            utils.save_object(file_path=self.data_transformation_config.transform_object_path, obj=transformation_pipleine)

            # Preparing Artifact
            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                transform_object_path = self.data_transformation_config.transform_object_path,
                transformed_train_path = self.data_transformation_config.transformed_train_path,
                transformed_test_path = self.data_transformation_config.transformed_test_path)

            logging.info(f"Data transformation object {data_transformation_artifact}")
            return data_transformation_artifact
            
        except Exception as e:
            raise MultiplicationException(e, sys)
