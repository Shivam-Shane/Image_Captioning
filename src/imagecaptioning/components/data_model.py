
import os
import pickle
from pathlib import Path
from src.imagecaptioning.config.configuration import DataModelConfig
from tensorflow.keras.preprocessing.text import Tokenizer #type:ignore
from tensorflow.keras.preprocessing.sequence import pad_sequences #type:ignore
from tensorflow.keras.utils import to_categorical #type:ignore
from tensorflow.keras.layers import Input,Dense,LSTM,Embedding,Dropout,add #type:ignore
from src.imagecaptioning.constants import *
from src.imagecaptioning.utils.common import read_yaml,update_yaml
from logger import logging
import warnings
warnings.filterwarnings("ignore")


class DataModel():
    def __init__(self,config=DataModelConfig):
        self.config=config
        self.parms=read_yaml(PARMS_FILE_PATH)

    def update_model_parameters(self):
        logging.info(f">>>> Inside {self.__class__.__name__}.{self.update_model_parameters.__name__}")
        all_captions=[]
        updated_parameters={}
        with open("artifacts\data_transformation\captions\captions.pkl","rb") as caption_file:
            logging.debug(f"Loading captions from path {os.path.join(self.config.data_captions,'captions.pkl')}")
            captions=pickle.load(caption_file)
            logging.debug(f"Loaded captions from path {os.path.join(self.config.data_captions,'captions.pkl')}")
            
            for key in captions:
                for caption in captions[key]:
                    all_captions.append(caption)

            tokenizer=Tokenizer()                # tokenizing the captions data to numerical values
            tokenizer.fit_on_texts(all_captions) # updates the internal vocabulary based on the word frequency
            vocab_size=len(tokenizer.word_index)+1 #+1 ensures an index reserved for padding

            max_length=max(len(caption.split()) for caption in all_captions)

            updated_parameters={"Model_Arguments.vocab_size":vocab_size
                                ,"Model_Arguments.max_length":max_length}
            update_yaml(PARMS_FILE_PATH,updated_parameters)
            
            logging.info(f">>>> End of {self.__class__.__name__}.{self.update_model_parameters.__name__}")
        

