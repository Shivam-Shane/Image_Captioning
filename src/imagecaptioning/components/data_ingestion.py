from logger import logging # type: ignore
from PIL import Image
import os
import shutil
from pathlib import Path
from src.imagecaptioning.config.configuration import DataIngestionConfig

class DataIngestion():
    def __init__(self,config:DataIngestionConfig):
        self.config = config
    def check_correpted_images(self):
        logging.info(f">>>>Inside {self.__class__.__name__}.{self.check_correpted_images.__name__}")
        dataingestionpath = Path(self.config.data_ingestion_path)
        dataset_dir = Path(self.config.data_path)
        dataset_dir=os.path.join(dataset_dir,"Images")
        corrupted_images = []
        for filename in os.listdir(dataset_dir):
            filepath = os.path.join(dataset_dir, filename)
            try:
                with Image.open(filepath) as img:
                    img.load()
                    
                    shutil.copy(filepath ,os.path.join(dataingestionpath,filename))
            except (IOError, OSError):
                corrupted_images.append(filename)
        logging.debug("Done checking for corrupted images")
        logging.info(f">>>>Ending {self.__class__.__name__}.{self.check_correpted_images.__name__}")
        return corrupted_images
    
