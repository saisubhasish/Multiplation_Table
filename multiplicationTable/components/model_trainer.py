from multiplicationTable.entity import artifact_entity,config_entity
from multiplicationTable.exception import MultiplicationException
from multiplicationTable.logger import logging
from typing import Optional
import os,sys 
from sklearn.ensemble import BaggingRegressor
from multiplicationTable import utils
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV



class ModelTrainer:

    def __init__(self, model_trainer_config:config_entity.ModelTrainerConfig,
                data_transformation_artifact:artifact_entity.DataTransformationArtifact):
        try:
            logging.info(f"{'>>'*20} Model Trainer {'<<'*20}")
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact

        except Exception as e:
            raise MultiplicationException(e, sys)
        
    def adj_r2_score(y, y_pred, n, p):
        '''
        This function takes y, y_pred, n and p value as input 
        ------------------------------------------------
        Returns: adjusted r2 performance value of a model
        '''
        r2 =  r2_score(y, y_pred)
        adj_r2 = 1-(1-r2)*(n-1)/(n-p-1)
        return adj_r2

    def fine_tune(self,x,y):
        """
        Hyper parameter tuning
        """
        try:
            # Defining parameters
            parameters = {
                'n_estimators': [10, 50, 100, 200, 300],
                'bootstrap': [True, False],
                'max_samples': [1,2,3,4,5], 
                'max_features': [1,2,3,4,5],
                'bootstrap_features': [True, False],
                'oob_score': [True, False],
                'warm_start': [True, False]
                } 
            
            br = BaggingRegressor()

            grid_search = GridSearchCV(estimator=br, param_grid=parameters, cv=10, n_jobs=-1, verbose=3)
            grid_search_xgb = grid_search_xgb.fit(x,y)
            BestParams = grid_search_xgb.best_params_
            
            return BestParams

        except Exception as e:
            raise MultiplicationException(e, sys)

    def train_model(self,x,y):
        """
        Model training
        """
        try:
            br =  BaggingRegressor()
            br.fit(x,y)
            return br

        except Exception as e:
            raise MultiplicationException(e, sys)

    def initiate_model_trainer(self,)->artifact_entity.ModelTrainerArtifact:
        """
        Preparing dataset
        """
        try:
            logging.info("Loading train and test array.")
            train_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_path)
            test_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_path)

            logging.info("Splitting input and target feature from both train and test arr.")
            x_train,y_train = train_arr[:,:-1],train_arr[:,-1]
            x_test,y_test = test_arr[:,:-1],test_arr[:,-1]

            #logging.info('Hyperparameter tuning using GridSearchCV')
            #Best_Params = self.fine_tune(x=x_train,y=y_train)
            #print(f"The best parameters for BaggingRegressor are : {Best_Params}")
            #logging.info(f"The best parameters for BaggingRegressor are : {Best_Params}")

            logging.info("Train the model")
            model = self.train_model(x=x_train,y=y_train)

            # Prediction and accuracy using training data
            logging.info("Calculating r2 train score")
            yhat_train = model.predict(x_train)
            r2_train_score  = r2_score(y_true=y_train, y_pred=yhat_train)

            # Prediction and acuracy using test data
            logging.info("Calculating r2 test score")
            yhat_test = model.predict(x_test)
            r2_test_score  = r2_score(y_true=y_test, y_pred=yhat_test)
            
            logging.info(f"train score:{r2_train_score} and tests score {r2_test_score}")
            # Check for overfitting or underfiiting on expected score
            logging.info("Checking if our model is underfitting or not")
            if r2_test_score<self.model_trainer_config.expected_score:
                raise Exception(f"Model is not good as it is not able to give \
                expected accuracy: {self.model_trainer_config.expected_score}: model actual score: {r2_test_score}")

            logging.info("Checking if our model is overfiiting or not")
            diff = abs(r2_train_score-r2_test_score)   # Checking the difference by removing -ve

            if diff>self.model_trainer_config.overfitting_threshold:
                raise Exception(f"Train and test score diff: {diff} is more than overfitting threshold {self.model_trainer_config.overfitting_threshold}")

            # Saving trained model to utils if it passes
            logging.info("Saving model object")
            utils.save_object(file_path=self.model_trainer_config.model_path, obj=model)

            # Prepare artifact
            logging.info("Prepare the artifact")
            model_trainer_artifact  = artifact_entity.ModelTrainerArtifact(model_path=self.model_trainer_config.model_path, 
            r2_train_score=r2_train_score, r2_test_score=r2_test_score)
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
            
        except Exception as e:
            raise MultiplicationException(e, sys)