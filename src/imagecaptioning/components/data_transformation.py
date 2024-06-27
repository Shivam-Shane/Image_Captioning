
import os
from pathlib import Path
from tqdm import tqdm
import pickle
import re
import numpy as np
from tensorflow.keras.preprocessing.image import load_img,img_to_array # type: ignore
from tensorflow.keras.applications.resnet50 import ResNet50,preprocess_input # type: ignore
from tensorflow.keras.models import Model # type: ignore
from src.imagecaptioning.config.configuration import DataTransformationConfig
from logger import logging
import warnings
warnings.filterwarnings("ignore")

#------------------------------------------------------------------------------------------------
class DataTransformation():
    def __init__(self,config:DataTransformationConfig):
        self.config=config
        
    def convert_images_to_features(self):
        """Converting images to features/Tf-idf for preprocessing
        Args: 
            None
        Returns: 
                Saves the features into pickle file.
        """
        logging.info(f">>>> Inside {self.__class__.__name__}.{self.convert_images_to_features.__name__}")
        try:
            
            self.model=ResNet50(weights='imagenet',include_top=True)
            # Taking only features layers from RESNET50 , not the last output fully connected layer layer
            self.feature_extracter=Model(inputs=self.model.input,outputs=self.model.layers[-2].output)    
            features={} # Dictonary for storing the features
            # Iterate over all images in the data ingestion path, preprocess images, extract features, and store them in features dictionary. 
            for image_name in tqdm(os.listdir(Path(self.config.data_ingestion_path)),desc='Processing'):
                img_path = os.path.join(Path(self.config.data_ingestion_path), image_name)
                if re.match(r'.*\.(jpg|jpeg|png)$', image_name, re.IGNORECASE):  # Check if the file is an image
                    image=load_img(img_path,target_size=(224,224))          # Loading the images 
                    image_array=img_to_array(image)                         # Converting images to array
                    image_array=np.expand_dims(image_array, axis=0)         # Reshapping data for model
                    preprocessed_image=preprocess_input(image_array)        # Processing input image using VGG16 preprocess_input function
                    # Extracting the features from the features extracter
                    features_extracted=self.feature_extracter.predict(preprocessed_image,verbose=0)
                    # Storing the extracted features with image IDs
                    features_extracted=features_extracted.reshape((2048,)) # Reshaping features to map renet50 model.
                    image_id =image_name.split('.')[0]    # Spliting the image name and taking its name as value['Img01','jpg']
                    features[image_id] =features_extracted
                
            logging.info(f"Saving features at path {self.config.data_transformation_save_features}")
            file_path = Path(os.path.join(self.config.data_transformation_save_features,"features.pkl"))             
            with open(file_path,"wb")as file:
                pickle.dump(features,file)   # saving the features into pickle file : features.pkl
                logging.info(f"Features saved at path {self.config.data_transformation_save_features}")
            
            logging.info(f">>>> Ending {self.__class__.__name__}.{self.convert_images_to_features.__name__}")
        except Exception as e:
            logging.error(e)
            raise e
    def map_captions_to_images(self):
        """Mapping Captions Id to Images ID
        Args: 
            Captions Id and Images to map
        Returns: 
                Saves the mapped features into pickle file.
        """
        logging.info(f">>>> Inside {self.__class__.__name__}.{self.map_captions_to_images.__name__}")
        try:
            mapping={}   # Dictionary for storing mapped captions
            with open(os.path.join(self.config.data_path,"captions.txt"),"r", encoding='utf-8') as file:
                next(file)                   # Next data so we don't have header in our data
                caption_document=file.read() # Storing all the caption
            # Mapping captions to images, splitting the line by comma and storing the image id and caption in dictionary.
            for line in tqdm(caption_document.split("\n")):
                token=line.split(",")       # image01.jpg, caption.....
                if len(token) < 2:
                    continue
                image_id,caption=token[0],token[1]
                image_id=image_id.split(".")[0]     # Removing extension from image id
                if image_id not in mapping:
                    mapping[image_id]=[]
                mapping[image_id].append(caption)   # Saving mapped captions

            def caption_cleaning(mapping):
                """Cleans all captions data
                Args: 
                    mapping: dictionary mapped IDs
                
                Return:
                        Cleaned captions data in form of pickle
                """
                cleaned_mapping={}
                for key,captions in mapping.items():
                    cleaned_captions=[]
                    for caption in captions:
                        caption=caption.lower() 
                        caption = re.sub(r"[^a-z\s]", "", caption)  # Using regex to replace non-alphabetic characters
                        caption="startcaption " + " ".join([word for word in caption.split() if len(word) >= 1]) + " endcaption" 
                        # added startcaption and endcaption to mark start and end of a caption
                        cleaned_captions.append(caption)
                    cleaned_mapping[key]=cleaned_captions
                return cleaned_mapping  # return all the cleaned captions

            cleaned_caption=caption_cleaning(mapping)# cleaning the caption list 

            logging.info(f"Saving mapped caption at path {self.config.data_transformation_save_captions}")         
            with open(os.path.join(self.config.data_transformation_save_captions,"captions.pkl"),"wb")as file:
                pickle.dump(cleaned_caption,file)  # saving captions as caption.pkl
                logging.info(f"Captions saved at path {self.config.data_transformation_save_captions} with name captions.pkl")

        except Exception as e:
            logging.error(e)
            raise e
#------------------------------------------------------------------------------------------------