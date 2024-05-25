from dataclasses import dataclass
from src.imagecaptioning.config.configuration import ConfigurationManager
from src.imagecaptioning.components.data_transformation import DataTransformation
from logger import logging

@dataclass
class DataTransformationPipeline():
    def main(self):
        get_configuratiomanger =ConfigurationManager()
        get_datatransformationconfig_details=get_configuratiomanger.get_data_transformation_config()
        datatransformation=DataTransformation(config=get_datatransformationconfig_details)
        datatransformation.convert_images_to_features()
        datatransformation.map_captions_to_images()