from logger import logging
import os
from src.imagecaptioning.config.configuration import DataTransformationConfig
from pathlib import Path
from tensorflow.keras.preprocessing.image import load_img,img_to_array # type: ignore
from tensorflow.keras.applications.vgg16 import VGG16,preprocess_input # type: ignore
from tensorflow.keras.models import Model # type: ignore
import warnings
warnings.filterwarnings("ignore")
class DataTransformation():
    def __init__(self,config:DataTransformationConfig):
        self.config=config
        

    def convert_images_to_features(self):
        logging.info(f">>>> Inside {self.__class__.__name__}.{self.convert_images_to_features.__name__}")
        try:
            self.model=VGG16(weights='imagenet',include_top=True)#fully connected layers responsible for classification are included.
            self.feature_extract=Model(inputs=self.model.input,outputs=self.model.layers[-2].output)# taking only features from , not the last output layer
            features={}
            for image_name in os.listdir(Path(self.config.data_ingestion_path)):
                img_path = os.path.join(Path(self.config.data_ingestion_path), image_name)
                image=load_img(img_path,target_size=(224,224)) #converting images to pixel
                image=img_to_array(image)
                image=image.reshape(1,image.shape[0],image.shape[1],image.shape[2])#reshapping data for model
                image=preprocess_input(image)
                # Extracting the features from the features extracter haiving layers from imagenet predefined dataset
                features_extracted=self.feature_extract.predict(image,verbose=0)
                #stroing the extracted features with image IDs
                image_id =image_name.split('.')[0]
                features[image_id] =features_extracted

        except Exception as e:
            logging.error(e)
            raise e