
import os
import pickle
from pathlib import Path
import numpy as np
from src.imagecaptioning.config.configuration import DataModelConfig
from tensorflow.keras.preprocessing.text import Tokenizer #type:ignore
from tensorflow.keras.preprocessing.sequence import pad_sequences #type:ignore
from tensorflow.keras.utils import to_categorical #type:ignore
from tensorflow.keras.layers import Input,Dense,Embedding,Dropout,add,BatchNormalization, GRU #type:ignore
from tensorflow.keras.optimizers import Adam #type:ignore
from tensorflow.keras.callbacks import ModelCheckpoint, LearningRateScheduler #type:ignore
from tensorflow.keras.models import Model,load_model  #type:ignore
from src.imagecaptioning.constants import *
from src.imagecaptioning.utils.common import read_yaml,update_yaml
from logger import logging
import warnings
warnings.filterwarnings("ignore")

#-----------------------------------------------------------------------------------------------------------------------------------------------
class DataModel():
    def __init__(self,config=DataModelConfig):
        self.config=config
        self.parms=read_yaml(PARMS_FILE_PATH)
        self.tokenizer=Tokenizer() 

        with open(Path(os.path.join(self.config.data_captions,'captions.pkl')),"rb") as caption_file:
            logging.debug(f"Loading captions from path {os.path.join(self.config.data_captions,'captions.pkl')}")
            self.captions=pickle.load(caption_file)
            logging.debug(f"Loaded captions from path {os.path.join(self.config.data_captions,'captions.pkl')}")
    
        with open(Path(os.path.join(self.config.data_features,'features.pkl')),"rb") as features_file:
            logging.debug(f"Loading features from path {os.path.join(self.config.data_features,'features.pkl')}")
            self.features=pickle.load(features_file)
            logging.debug(f"Loaded features from path {os.path.join(self.config.data_features,'features.pkl')}")

    def update_model_parameters(self):
        """Updates Model arguments for training
        Args:
            captions, features taking from pickle file
        Returns: 
            None
        """
        logging.info(f">>>> Inside {self.__class__.__name__}.{self.update_model_parameters.__name__}")
        
        all_captions=[]
        updated_parameters={}  # Empty dict for storing updated parameters

        for key in self.captions:              # Iterate over all captions document to get key
            for caption in self.captions[key]: # Iterate over all caption with specific key[image name]
                all_captions.append(caption)   # Append all captions to list.

        logging.debug(f"Total number of captions processed: {len(all_captions)}")

        self.tokenizer.fit_on_texts(all_captions)       # Updates the internal vocabulary based on the word frequency
        vocab_size=len(self.tokenizer.word_index)+1     # +1 numerical ensures an index reserved for padding
        max_length=max(len(caption.split()) for caption in all_captions)

        logging.debug(f"Max length{max_length} Vocabulary size: {vocab_size}")

        updated_parameters={"Model_Arguments.vocab_size":vocab_size
                            ,"Model_Arguments.max_length":max_length}
        update_yaml(PARMS_FILE_PATH,updated_parameters)     # Updating the model parameters by calling the update_yaml function
        
        tokenizer_json = self.tokenizer.to_json()           # Save the tokenizer
        logging.info("Saving tokenizer file in json format")
        with open(Path(os.path.join(self.config.data_model_tokenizer,'tokenizer.json')), 'w') as f:
            f.write(tokenizer_json)
            logging.info(f"Tokenizer saved to {self.config.data_model_tokenizer} ")

        logging.info(f">>>> End of {self.__class__.__name__}.{self.update_model_parameters.__name__}")
        
    def create_captions_sequence(self,captions_list, image):
        """ Creates caption sequence  
        Args:
            Captions_list: list of all captions
            Image: all images
        Returns:
            Numpy arrays
        Raises:
            Exception: if anything goes wrong
        """
        logging.debug(f">>>> Inside {self.__class__.__name__}.{self.update_model_parameters.__name__}")
        try:
            X1, X2, y = list(), list(), list()  # Initialize empty lists to hold image features, input sequences, and output words
            for caption in captions_list:       # Iterate over each caption
                seq = self.tokenizer.texts_to_sequences([caption])[0]   # Convert the caption to a sequence of integers

                for i in range(1, len(seq)):                    # Create multiple input-output pairs from the caption
                    in_seq, out_seq = seq[:i], seq[i]           # Split the sequence into input (first i words) and output (i-th word)
                    in_seq = pad_sequences([in_seq], maxlen=self.parms.Model_Arguments.max_length)[0]           # Pad the input sequence to the maximum length
                    out_seq = to_categorical([out_seq], num_classes=self.parms.Model_Arguments.vocab_size)[0]   # One-hot encode the output word
                    X1.append(image)                            # Adding the image feature to X1
                    X2.append(in_seq)                           # Adding the input sequence to X2
                    y.append(out_seq)                           # Adding the one-hot encoded output word to y
            logging.debug(f">>>> End of {self.__class__.__name__}.{self.create_captions_sequence.__name__}")      
            return np.array(X1), np.array(X2), np.array(y)      # Return the arrays as numpy arrays
        except Exception as e:
            raise e

    def data_generator(self,captions, image_features):      # Ensure that not all dataset is loaded at once in memory
        """ Generates Data in batches for model
        Args:
            captions: list of captions
            image_features: list of image features
        Returns :
                batchs of data to model
        """
        logging.info(f">>>> Inside {self.__class__.__name__}.{self.data_generator.__name__}")
        
        while True:
            logging.debug("Generating batch fixes for training")
            keys=list(captions.keys())                        # List all the images ID
            np.random.shuffle(keys)                           # Shuffling the keys to ensure randomness
            batch_size=self.parms.Model_Arguments.batch_size  # Getting the batch size
            for i in range(0, len(keys),batch_size):          # Iterate over the keys in the batch_size increament
                X1, X2, y = list(), list(), list()            # Empty list for current batch
                for j in range(i,min(i+batch_size,len(keys))) : # for each key in the current batch
                    key=keys[j]
                    image=image_features[key]                   # Get the image feature for the current key
                    if image.shape != (2048,):
                        logging.critical(f"Expected image shape (2048,), got {image.shape}")
                    captions_list=captions[key]                # Get the captions for the current key
                    in_img,in_seq,out_word=self.create_captions_sequence(captions_list,image) # Create the sequence
                    X1.extend(in_img)                       # extend the image
                    X2.extend(in_seq)                       # extend the sequence
                    y.extend(out_word)                      # extend the output caption
                yield ({'input_layer': np.array(X1), 'input_layer_1': np.array(X2)}, np.array(y))
                
            logging.info(f">>>> End of {self.__class__.__name__}.{self.data_generator.__name__}")

    def model_definition(self):
        """ Model definition
        Args:  
            None
        Returns: 
            modelwrappers
        """
        logging.info(f">>>> Inside {self.__class__.__name__}.{self.model_definition.__name__}")
        image_inputs1 = Input(shape=(2048,))  # Image Layer
        feature1 = Dropout(0.5)(image_inputs1)
        feature2 = Dense(512, activation="relu")(feature1)
        feature2 = BatchNormalization()(feature2)
        
        # Caption processing
        text_inputs2 = Input(shape=(self.parms.Model_Arguments.max_length,))  # Caption Layer
        seq2 = Embedding(self.parms.Model_Arguments.vocab_size, 256, mask_zero=True)(text_inputs2)
        seq2 = Dropout(0.5)(seq2)
        seq2 = GRU(512, return_sequences=True)(seq2)
        seq2 = GRU(512)(seq2)
        
        # Decoder (combining image features and text features)
        decoder1 = add([feature2, seq2])
        decoder1 = Dense(512, activation="relu")(decoder1)
        decoder1 = BatchNormalization()(decoder1)
        outputs = Dense(self.parms.Model_Arguments.vocab_size, activation="softmax")(decoder1)
        
        model = Model(inputs=[image_inputs1, text_inputs2], outputs=outputs)
        model.compile(loss="categorical_crossentropy", optimizer=Adam(learning_rate=1e-4))

        logging.debug(f"Model Summary{model.summary}")
        logging.info(f">>>> End of {self.__class__.__name__}.{self.model_definition.__name__}")
        return model

    def model_training(self):
        """   Train the model
        Args: 
            None
        Returns: 
                None
        Raises:
            Exception: if anything goes wrong
        """
        logging.info(f">>>> Inside {self.__class__.__name__}.{self.model_training.__name__}")

        steps=len(self.captions) // self.parms.Model_Arguments.batch_size
        logging.debug("Calling model definition")
        model=self.model_definition()

        # Define the checkpoint callback
        checkpoint_callback = ModelCheckpoint(
            filepath=os.path.join(self.config.data_model_path, 'model_checkpoint.keras'),  # File path where the model weights will be saved
            monitor='loss',              # Monitor the training loss
            save_best_only=True,         # Save only the best model
            save_weights_only=False,     # Save the full model (architecture + optimizer state + weights)
            verbose=1                    # message when a model checkpoint is saved
        )
        def learning_rate_scheduler(epoch, lr):
            if epoch > 10:
                return lr * 0.1
            return lr

        lr_scheduler_callback = LearningRateScheduler(learning_rate_scheduler)  # learning rate scheduler 
        
        # Combineing all callbacks
        callbacks_list = [checkpoint_callback, lr_scheduler_callback]

        logging.debug(f"starting training in batches with batch size {self.parms.Model_Arguments.batch_size}")
        is_checkpoint = "No checkpoint found, starting training from scratch"
        if os.path.exists(Path(os.path.join(self.config.data_model_path, 'model_checkpoint.keras'))):
            model = load_model(Path(os.path.join(self.config.data_model_path, 'model_checkpoint.keras')))
            is_checkpoint="Starting training from checkpoint"
        logging.info(is_checkpoint)

        model.fit(
            self.data_generator( self.captions, self.features),
            epochs=self.parms.Model_Arguments.epochs,         # Number of epochs to train
            steps_per_epoch=steps,                            # Number of steps
            verbose=1,                                        # On terminal output
            callbacks=callbacks_list                          # Callbacks list [checkpoint, LRS]
            )
        try:
            logging.info("Saving model pickle to keras file")
            model.save(os.path.join(self.config.data_model_path,"model.keras"))  # saving the last model in pickle file
        except Exception as e:
                raise e 
        logging.info(f">>>> End of {self.__class__.__name__}.{self.model_training.__name__}")
#--------------------------------------------------------------------------------------------------------------------------------------------