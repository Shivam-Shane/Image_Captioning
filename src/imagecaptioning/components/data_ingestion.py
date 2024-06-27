from PIL import Image
import os
import shutil
from pathlib import Path
from src.imagecaptioning.config.configuration import DataIngestionConfig
from logger import logging

class DataIngestion():
    def __init__(self,config:DataIngestionConfig):
        self.config = config
    def check_correpted_images(self):
        """Check if the image is valid and good enough for models

        Args:
            None (default)
        return:
            correpted_images[list] 
        """
        logging.info(f">>>>Inside {self.__class__.__name__}.{self.check_correpted_images.__name__}")
        dataingestionpath = Path(self.config.data_ingestion_path)
        dataset_dir = Path(self.config.data_path)
        dataset_dir=os.path.join(dataset_dir,"Images")
        corrupted_images = []
        try:
            for filename in os.listdir(dataset_dir):          # Gets the filename from the dataset directory
                filepath = os.path.join(dataset_dir, filename) # Gets the file path to open
                try:
                    with Image.open(filepath) as img:
                        img.load()
                                                        # Moved the image to new location if its valid
                        shutil.copy(filepath ,os.path.join(dataingestionpath,filename)) 
                except (IOError, OSError):
                    corrupted_images.append(filename)

            logging.info(f">>>>Ending {self.__class__.__name__}.{self.check_correpted_images.__name__}")
            return corrupted_images
        except Exception as e:
            raise e
#----------------------------------------------------------------------------------------------