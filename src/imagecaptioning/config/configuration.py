from src.imagecaptioning.constants import *
from src.imagecaptioning.utils.common import read_yaml,create_directories
from src.imagecaptioning.entity import DataIngestionConfig,DataTransformationConfig
from logger import logging


class ConfigurationManager():
    def __init__(self,
                CONFIG_FILE_PATH=CONFIG_FILE_PATH,
                PARMS_FILE_PATH=PARMS_FILE_PATH):
        
        self.config_data=read_yaml(CONFIG_FILE_PATH)
        self.parms=read_yaml(PARMS_FILE_PATH)
        create_directories([self.config_data.artifacts_root])


        logging.info(self.config_data.data_ingestion)

    def get_data_ingestion_config(self)-> DataIngestionConfig:
        logging.info(f">>>>Inside {self.__class__.__name__}.{self.get_data_ingestion_config.__name__}")
        config_ingestion_data=self.config_data.data_ingestion
        create_directories([config_ingestion_data.data_path,config_ingestion_data.data_ingestion_path])
        

        data_ingestion_config_details =DataIngestionConfig(
            data_path=config_ingestion_data.data_path,
            data_ingestion_path=config_ingestion_data.data_ingestion_path
        )
        logging.info(f">>>> End of {self.__class__.__name__}.{self.get_data_ingestion_config.__name__}")
        return data_ingestion_config_details
    
    def get_data_transformation_config(self)->DataTransformationConfig:
        logging.info(f">>>>Inside {self.__class__.__name__}.{self.get_data_transformation_config.__name__}")
        config_transformation_data=self.config_data.data_transformation
        create_directories([config_transformation_data.data_ingestion_path,config_transformation_data.data_transformation_path])

        data_transformation_config_detail=DataTransformationConfig(
            data_ingestion_path=config_transformation_data.data_ingestion_path,
            data_transformation_path=config_transformation_data.data_transformation_path

        )
        logging.info(f">>>> End of {self.__class__.__name__}.{self.get_data_transformation_config.__name__}")
        return data_transformation_config_detail