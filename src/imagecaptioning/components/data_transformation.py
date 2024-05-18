
import os
from pathlib import Path
from tqdm import tqdm
import pickle
from tensorflow.keras.preprocessing.image import load_img,img_to_array # type: ignore
from tensorflow.keras.applications.vgg16 import VGG16,preprocess_input # type: ignore
from tensorflow.keras.models import Model # type: ignore
from src.imagecaptioning.config.configuration import DataTransformationConfig
from logger import logging
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
            for image_name in tqdm(os.listdir(Path(self.config.data_ingestion_path)),desc='Processing'):
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
            logging.debug(f"Saving features at path {self.config.data_transformation_save_features}")
            file_path = Path(os.path.join(self.config.data_transformation_save_features,"features.pkl"))             
            with open(file_path,"wb")as file:
                pickle.dump(features,file)
                logging.info(f"Features saved at path {self.config.data_transformation_save_features}")
            
            logging.info(f">>>> Ending {self.__class__.__name__}.{self.convert_images_to_features.__name__}")
        except Exception as e:
            logging.error(e)
            raise e
    def map_captions_to_images(self):
        logging.info(f">>>> Inside {self.__class__.__name__}.{self.map_captions_to_images.__name__}")
        try:
            mapping={}
            with open(os.path.join(self.config.data_path,"caption.txt"),"r") as file:
                next(file)
                caption_document=file.read() #storing all the captions
            for line in tqdm(caption_document.split("\n")):
                token=line.split(",")
                image_id,caption=token[0],token[1]
                #Removing extextion from image id
                image_id=image_id.split(".")[0]
                # Converting caption list to string
                caption=" ".join(caption)
                #list if needed
                if image_id not in mapping:
                    mapping[image_id]=[]
                mapping[image_id].append(caption)
            def caption_cleaining(mapping):
                for key,caption in mapping.items():
                    for i in range(len(caption)):
                        caption=caption[i]
                        caption=caption.lower()
                        caption=caption.replace("[^A-Za-z]","")
                        # caption=caption.replace("\s+","")# additional spaces removal
                        caption="<start>"+" ".join([word for word in caption.split() if len(word)>=1])+"<end>"
            
            caption_cleaining(mapping)# cleaning the caption list   
                        
        except Exception as e:
            logging.error(e)
            raise e