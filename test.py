import os
import random
from PIL import Image
from src.imagecaptioning.components import data_model
from dataclasses import dataclass
from src.imagecaptioning.config.configuration import ConfigurationManager
from src.imagecaptioning.components.data_predictor import Caption_Predictor

class Caption_validator():
    def main(image):
       get_configuratiomanger =ConfigurationManager()
       get_datamodelconfig_details=get_configuratiomanger.get_data_model_config()
       datapredictor=Caption_Predictor(config=get_datamodelconfig_details)
       feature=datapredictor.preprocess_image(image)
       caption=datapredictor.generates_captions(feature)
       return caption
    
    def eposc(self,n=1):
        image_path="artifacts\data_ingestion"
        caption_list=[]
        image_list=[]
        
        with open("dataset/captions.txt","r", encoding='utf-8')as file: 
            next(file)
            caption_dc=file.read()
        caption_random=random.sample(caption_dc.split('\n'),n)
        for line in caption_random: 
                token=line.split(",")
                if len(token) < 2:
                    continue
                image_id,caption=token[0],token[1] 
                caption_list.append(caption),image_list.append(image_id)
        
        for i in range(n):
            file_path=os.path.join(image_path, image_list[i])
            print(file_path)
            y_caption= Caption_validator.main(file_path)
            y_caption = y_caption.strip('startcaption').strip('endcaption')
            print("Actual",caption_list[i])
            print("Predicted",y_caption)

if __name__ == '__main__':
   ob=Caption_validator()
   ob.eposc(6)