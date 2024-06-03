from dataclasses import dataclass
from src.imagecaptioning.config.configuration import ConfigurationManager
from src.imagecaptioning.components.data_predictor import Caption_Predictor

@dataclass
class DataPredictionPipeline():
    def main(self):
       get_configuratiomanger =ConfigurationManager()
       get_datamodelconfig_details=get_configuratiomanger.get_data_model_config()
       datapredictor=Caption_Predictor(config=get_datamodelconfig_details)
       feature=datapredictor.preprocess_image()
       datapredictor.generates_captions(feature)
       