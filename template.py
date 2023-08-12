import os    # template for creating directory in a project
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')


project_name = "multiplicationTable"

list_of_files = [
    ".github/workflows/.gitkeep",
    ".github/workflows/main.yaml",
    f"{project_name}/__init__.py",
    f"{project_name}/components/__init__.py",
    f"{project_name}/components/data_ingestion.py",
    f"{project_name}/components/data_validation.py",
    f"{project_name}/components/data_transformation.py",
    f"{project_name}/components/model_trainer.py",
    f"{project_name}/components/model_evaluation.py",
    f"{project_name}/components/model_pusher.py",
    f"{project_name}/entity/__init__.py",
    f"{project_name}/entity/config_entity.py",
    f"{project_name}/entity/artifact_entity.py",
    f"{project_name}/pipeline/__init__.py",
    f"{project_name}/pipeline/training_pipeline.py",
    f"{project_name}/pipeline/prediction_pipeline.py",
    f"{project_name}/config.py",
    f"{project_name}/exception.py",
    f"{project_name}/logger.py",
    f"{project_name}/predictor.py",
    f"{project_name}/utils.py",
    "airflow/dags/prediction_pipeline.py",
    "airflow/dags/training_pipeline.py",
    ".gitignore",
    ".dockerignore",
    "app.py",
    "docker-compose.yaml",
    "Dockerfile",
    "requirements.txt",
    "setup.py",
    "start.sh",
    "test.py"
]


for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory:{filedir} for the file {filename}")

    
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath,'w') as f:
            pass
            logging.info(f"Creating empty file: {filepath}")


    
    else:
        logging.info(f"{filename} is already exists")

