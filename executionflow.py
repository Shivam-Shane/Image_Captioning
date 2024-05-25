from src.imagecaptioning.constants import *
from src.imagecaptioning.utils.common import read_yaml
from logger import logging
from src.imagecaptioning.entity import ExecuationFlowConfig

class Executionflow():
    def __init__(self,
        config_filepath=CONFIG_FILE_PATH):
        logging.info(f">>>> Inside {self.__class__.__name__}.{self.__init__.__name__}")
        self.config=read_yaml(config_filepath), # Reading config yaml file for execution flow
    
    def get_data_for_executionflow(self)->ExecuationFlowConfig: #Returing object of type ExecutionFlowConfig needed to our entity module
        """Get keys for execution flow .
        Args:
            None
        Returns:
        ExecutionflowConfig: Having values for corresponding keys related to execution flow
        """
        logging.info(f">>>> Inside {self.__class__.__name__}.{self.get_data_for_executionflow.__name__}")
        config=self.config[0].execution_flow
        execution_flow_config=ExecuationFlowConfig(
                                data_ingestion_flow=config.data_ingestion_flow,
                                data_transformation_flow=config.data_transformation_flow,
                                model_trainer_flow=config.model_trainer_flow,
                                model_evaluation_flow=config.model_evaluation_flow
                                # add more execution flow here, and in entity and config.yaml files
        )
        return execution_flow_config