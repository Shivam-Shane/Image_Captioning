import os
import numpy as np
import re
from src.imagecaptioning.config.configuration import DataModelConfig
from tensorflow.keras.preprocessing.text import tokenizer_from_json # type:ignore
from tensorflow.keras.preprocessing.sequence import pad_sequences # type:ignore
from tensorflow.keras.preprocessing.image import load_img, img_to_array # type:ignore
from tensorflow.keras.applications.resnet50 import ResNet50,preprocess_input # type:ignore
from tensorflow.keras.models import Model, load_model # type:ignore
from src.imagecaptioning.constants import *
from src.imagecaptioning.utils.common import read_yaml
from logger import logging

# -----------------------------------------------------------------------------------------------------------------------------------------------
class Caption_Predictor:
    # class variables
    _runonce = False
    _feature_extractor = None
    _model = None
    _tokenizer = None

    def __init__(self, config=DataModelConfig):
        self.config = config
        self.parms = read_yaml(PARMS_FILE_PATH)
        
        if not Caption_Predictor._runonce: # making sure we don't call this twice reducing workload time
            try:
                logging.info(f"Loading saved model keras file from path {self.config.data_model_path}")
                Caption_Predictor._model = load_model(Path(os.path.join(self.config.data_model_path, "model.keras")))

                logging.info(f"Loading feature tokenizer file from path {self.config.data_model_tokenizer}")
                with open(Path(os.path.join(self.config.data_model_tokenizer, "tokenizer.json"))) as f:
                    tokenizer_json = f.read()
                Caption_Predictor._tokenizer = tokenizer_from_json(tokenizer_json)

                # Load the Resnet50 model, pre-trained on ImageNet dataste
                self.renet_model = ResNet50(include_top=True, weights='imagenet')
                # Extracting features layer from the resnet50 model
                Caption_Predictor._feature_extractor = Model(inputs=self.renet_model.inputs, outputs=self.renet_model.layers[-2].output)
                Caption_Predictor._runonce = True
            except Exception as e:
                raise e

        # class attributes to instance attributes for convenience
        self.model = Caption_Predictor._model
        self.tokenizer = Caption_Predictor._tokenizer
        self.feature_extractor = Caption_Predictor._feature_extractor

    def preprocess_image(self, input_image):
        """ Transform the input image
        Args:
            input_image:Path
        Returns:
                features_extracted: Transformed input_image features
        Raises:
            Exception: if anything goes wrong
        """
        try:
            logging.info(f"<<<< Start of {self.__class__.__name__}.{self.preprocess_image.__name__}")
            image = load_img(input_image, target_size=(224, 224))  # Loading the image
            image = img_to_array(image)             # Converting images to pixel
            image = np.expand_dims(image, axis=0)   # Reshaping data for model
            image = preprocess_input(image)         # Processing input image using VGG16 preprocess_input function
            # Extracting the features from the features extractor having layers from ImageNet predefined dataset
            features_extracted = self.feature_extractor.predict(image, verbose=0)
            logging.info(f">>>> End of {self.__class__.__name__}.{self.preprocess_image.__name__}")
            return features_extracted
        except Exception as e:
            raise e

    def generates_captions(self, feature_image):
        """Generates Captions for the given feature image
        Args:
            FeatureImage: Transformed image features
        Returns:
                Caption: Captions for the given feature image
        Raises:
            Exception: if anything goes wrong
        """
        logging.info(f"<<<< Start of {self.__class__.__name__}.{self.generates_captions.__name__}")

        in_text = "startcaption"
        try:
            for i in range(self.parms.Model_Arguments.max_length):
                # Convert the input text to a sequence of integers using the tokenizer
                sequence = self.tokenizer.texts_to_sequences([in_text])[0]
                # Padding the sequence to ensure it has the required length
                sequence = pad_sequences([sequence], maxlen=self.parms.Model_Arguments.max_length)
                yhat_prob = self.model.predict([feature_image, sequence], verbose=0) # 'verbose=0' suppresses the output of the prediction process
                yhat_max_prob_index = np.argmax(yhat_prob)  # Index of the highest probability in the predicted output for current sequence
                word = self.tokenizer.index_word[yhat_max_prob_index] 
                # Retrieve the word corresponding to the predicted index from the tokenizer's index_word vocabulary
                if word is None:
                    logging.info('word not found')
                    break
                in_text += ' ' + word
                if word == 'endcaption':
                    logging.info('endcaption found')
                    break
            logging.info(f">>>> End of {self.__class__.__name__}.{self.generates_captions.__name__}")
            logging.info(in_text)
            pattern = r'startcaption\s*(.*?)\s*endcaption'  # pattern for removing unnecessary words[startcaption, endcaption].
            cleaned_text = re.sub(pattern, r'\1', in_text, flags=re.DOTALL)  
            return cleaned_text.strip()  # any leading and trailing whitespace removed
        except Exception as e:
            raise e
# -----------------------------------------------------------------------------------------------------------------------------------------------