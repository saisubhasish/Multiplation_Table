import os, sys
from multiplicationTable.logger import logging
from multiplicationTable.exception import MultiplicationException
from multiplicationTable.predictor import ModelResolver
from multiplicationTable.entity.config_entity import ModelPusherConfig
from multiplicationTable.utils import save_object, load_object
from multiplicationTable.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact, ModelPusherArtifact

class ModelPusher:

    def __init__(self,model_pusher_config:ModelPusherConfig,
        data_transformation_artifact:DataTransformationArtifact,
        model_trainer_artifact:ModelTrainerArtifact):
        try:
            logging.info(f"{'>>'*20} Model Pusher {'<<'*20}")
            self.model_pusher_config=model_pusher_config
            self.data_transformation_artifact=data_transformation_artifact
            self.model_trainer_artifact=model_trainer_artifact
            self.model_resolver = ModelResolver(model_registry=self.model_pusher_config.saved_model_dir)
        except Exception as e:
            raise MultiplicationException(e, sys)

    def initiate_model_pusher(self)->ModelPusherArtifact:
        try:
            # Load object 
            logging.info("Loading transformer, model and taarget encoder")
            transformer = load_object(file_path=self.data_transformation_artifact.transform_object_path)
            model = load_object(file_path=self.model_trainer_artifact.model_path)

            # Model pusher dir
            logging.info("Saving model into model pusher directory")
            save_object(file_path= self.model_pusher_config.pusher_transformer_path, obj=transformer)
            save_object(file_path= self.model_pusher_config.pusher_model_path, obj=model)

            # Getting or fetching the directory location to save latest model in different directory in each run
            logging.info("Saving model in saved model dir")
            transformer_path = self.model_resolver.get_latest_save_transformer_path()
            model_path = self.model_resolver.get_latest_save_model_path()

            # Saved model dir outside artifact to use in prediction pipeline
            logging.info('Saving model outside of artifact directory')
            save_object(file_path=transformer_path, obj=transformer)
            save_object(file_path=model_path, obj=model)

            model_pusher_artifact = ModelPusherArtifact(pusher_model_dir=self.model_pusher_config.pusher_model_dir, 
                                                        saved_model_dir=self.model_pusher_config.saved_model_dir)
            logging.info(f"Model pusher artifact : {model_pusher_artifact}")

            return model_pusher_artifact

        except Exception as e:
            raise MultiplicationException(e, sys)
