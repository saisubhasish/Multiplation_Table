from multiplicationTable.entity import config_entity, artifact_entity
from multiplicationTable.exception import MultiplicationException
from multiplicationTable.predictor import ModelResolver
from multiplicationTable.config import TARGET_COLUMN
from multiplicationTable.utils import load_object
from sklearn.metrics import r2_score
from multiplicationTable.logger import logging
import pandas as pd
import os, sys

 

class ModelEvaluation:

    def __init__(self,
        model_eval_config:config_entity.ModelEvaluationConfig,
        data_validation_artifact:artifact_entity.DataValidationArtifact,
        data_transformation_artifact:artifact_entity.DataTransformationArtifact,
        model_trainer_artifact:artifact_entity.ModelTrainerArtifact):
        try:
            logging.info(f"{'>>'*20}  Model Evaluation {'<<'*20}")
            self.model_eval_config=model_eval_config
            self.data_validation_artifact=data_validation_artifact
            self.data_transformation_artifact=data_transformation_artifact
            self.model_trainer_artifact=model_trainer_artifact
            self.model_resolver = ModelResolver()
        except Exception as e:
            raise MultiplicationException(e,sys)

    def initiate_model_evaluation(self)->artifact_entity.ModelEvaluationArtifact:
        try:
            # If saved model folder has model then we will compare 
            # Which model is best trained or the model from saved model folder

            logging.info("If saved model folder has model the we will compare "
            "which model is best, trained or the model from saved model folder")
            latest_dir_path = self.model_resolver.get_latest_dir_path()
            if latest_dir_path==None:                                 # If there is no saved_models then we will accept the currnt model
                model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True,
                improved_accuracy=None)                                                              
                logging.info(f"Model evaluation artifact: {model_eval_artifact}")
                return model_eval_artifact

            # Finding location of transformer and model from saved_models dir
            logging.info("Finding location of transformer and model from saved_models dir")
            transformer_path = self.model_resolver.get_latest_transformer_path()
            model_path = self.model_resolver.get_latest_model_path()

            # Loading previous trained  objectsfrom saved_models dir
            logging.info("Previous trained objects of transformer and model from saved_models dir")
            transformer = load_object(file_path=transformer_path)
            model = load_object(file_path=model_path)

            logging.info("Currently trained model objects")
            # Currently trained model objects
            current_transformer = load_object(file_path=self.data_transformation_artifact.transform_object_path)
            current_model  = load_object(file_path=self.model_trainer_artifact.model_path)
            

            # Reading test file
            test_df = pd.read_csv(self.data_validation_artifact.test_file_path)
            # output label
            target_df = test_df[TARGET_COLUMN]
            y_true=target_df
            
            # Accuracy using previous trained model
            input_feature_name = list(transformer.feature_names_in_)
            input_arr = transformer.transform(test_df[input_feature_name])
            y_pred = model.predict(input_arr)
            # Label decoding with 5 values to get actual string
            # print(f"Prediction using previous model: {transformer.inverse_transform(y_pred[:5])}") # Not Required
            print(y_pred)
            previous_model_score = r2_score(y_true=y_true, y_pred=y_pred)
            logging.info(f"Accuracy using previous trained model: {previous_model_score}")

            # Accuracy using current trained model
            input_feature_name = list(current_transformer.feature_names_in_)
            input_arr =current_transformer.transform(test_df[input_feature_name])
            y_pred = current_model.predict(input_arr)
            # Label decoding with 5 values to get actual string 
            # print(f"Prediction using trained model: {current_transformer.inverse_transform(y_pred[:5])}") # Not required
            print(y_pred)
            current_model_score = r2_score(y_true=y_true, y_pred=y_pred)
            logging.info(f"Accuracy using current trained model: {current_model_score}")
            if current_model_score<=previous_model_score:
                logging.info("Current trained model is not better than previous model")
                raise Exception("Current trained model is not better than previous model")

            model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True,
            improved_accuracy=current_model_score-previous_model_score)
            
            # Improved accuracy
            logging.info(f"Model eval artifact: {model_eval_artifact}")
            return model_eval_artifact
        except Exception as e:
            raise MultiplicationException(e,sys)
