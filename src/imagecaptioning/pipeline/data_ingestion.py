from dataclasses import dataclass
from src.imagecaptioning.config.configuration import ConfigurationManager
from src.imagecaptioning.components.data_ingestion import DataIngestion
from logger import logging

@dataclass
class DataIngestionPipeline():
    def main(self):
       get_configuratiomanger =ConfigurationManager()
       get_dataingestionconfig_details=get_configuratiomanger.get_data_ingestion_config()
       dataingestion=DataIngestion(config=get_dataingestionconfig_details)
       dataingestion.check_correpted_images()