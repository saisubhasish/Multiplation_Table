import pandas as pd 
import numpy as np
import os, sys
import yaml
import dill    # To store python object as a file like pkl
from multiplicationTable.logger import logging
from multiplicationTable.config import mongo_client
from multiplicationTable.exception import MultiplicationException


def get_collection_as_dataframe(database_name:str,collection_name:str)->pd.DataFrame:
    """
    Description: This function return collection as dataframe
    =========================================================
    Params:
    database_name: database name
    collection_name: collection name
    =========================================================
    return Pandas dataframe of a collection
    """
    try:    
        logging.info(f"Reading data from database: {database_name} and collection: {collection_name}")
        df = pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        logging.info(f"Found columns: {df.columns}")
        if "_id" in df.columns:
            logging.info(f"Dropping column: _id ")
            df = df.drop("_id",axis=1)
        logging.info(f"Row and columns in df: {df.shape}")
        return df
    except Exception as e:
        raise MultiplicationException(e, sys)
    

def write_yaml_file(file_path,data:dict):
    """
    Description: Creating yaml report for validation status of each column
    =========================================================
    Params:
    file_path: file path
    data: data to write in report
    =========================================================
    """
    try:
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir,exist_ok=True)
        with open(file_path,"w") as file_writer:
            yaml.dump(data,file_writer)
    except Exception as e:
        raise MultiplicationException(e, sys)

def convert_columns_float(df:pd.DataFrame)->pd.DataFrame:
    """
    Description: Converting column to float type 
    =========================================================
    Params:
    df: data frame
    =========================================================
    return Pandas dataframe 
    """
    try:
        for column in df.columns:
            df[column] = df[column].astype('float')
        return df
    except Exception as e:
        raise MultiplicationException(e, sys)
    
def remove_extra_characters_from_column(df:pd.DataFrame)->pd.DataFrame:
    """
    Description: Removing extra characters from column
    =========================================================
    Params:
    df: data frame
    =========================================================
    return Pandas dataframe 
    """
    try:
        for column in df.columns:
            df[column] = df[column].map(lambda x: str(x).strip().rstrip('a').rstrip('b').rstrip('c').rstrip('d').rstrip('e'))
        return df
    except Exception as e:
        raise MultiplicationException(e, sys)


def save_object(file_path: str, obj: object) -> None:
    """
    Saving object 
    """
    try:
        logging.info("Entered the save_object method of utils")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
        logging.info("Exited the save_object method of utils")
    except Exception as e:
        raise MultiplicationException(e, sys) from e


def load_object(file_path: str, ) -> object:
    """
    Loading object
    """
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} is not exists")
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise MultiplicationException(e, sys) from e


def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise MultiplicationException(e, sys) from e


def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise MultiplicationException(e, sys) from e