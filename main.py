import sys
from multiplicationTable.exception import MultiplicationException
from multiplicationTable.pipeline.training_pipeline import start_training_pipeline

FILE_PATH = "multiplicationTable.csv"

if __name__ == '__main__':
    try:
        start_training_pipeline()

    except Exception as e:
        raise MultiplicationException(e, sys)
