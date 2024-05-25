from dataclasses import dataclass
from src.imagecaptioning.config.configuration import ConfigurationManager
from src.imagecaptioning.components.data_model import DataModel
from logger import logging

@dataclass
class DataModelPipeline():
    def main(self):
        get_configuratiomanger =ConfigurationManager()
        get_datamodelconfig_details=get_configuratiomanger.get_data_model_config()
        datamodel=DataModel(config=get_datamodelconfig_details)
        datamodel.update_model_parameters()