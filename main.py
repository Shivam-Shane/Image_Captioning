# from src.imagecaptioning.components import data_ingestion
import time
from logger import logging
from src.imagecaptioning.pipeline.data_ingestion import DataIngestionPipeline
from src.imagecaptioning.pipeline.data_transformation import DataTransformationPipeline
from src.imagecaptioning.pipeline.data_model import DataModelPipeline
from executionflow import Executionflow
import warnings
warnings.filterwarnings("ignore")

#----------------------------------------------------------------
logging.info(">>>> Application Started")
get_execuationflow=Executionflow()
get_execuationflow=get_execuationflow.get_data_for_executionflow()
try:
    start=time.time()
    STAGE_NAME="DATA INGESTION"
    if get_execuationflow.data_ingestion_flow==True:
        logging.info(f">>>>>>>>>>>>>>> Starting {STAGE_NAME} pipeline")
        Get_data_ingetsion_pipeline=DataIngestionPipeline()
        Get_data_ingetsion_pipeline.main()
        logging.info(f"<<<<<<<<<<<<<<< Stage {STAGE_NAME} is completed successfully")
    else:
         logging.info(f"-------------- Stage {STAGE_NAME} is skipped.")

    STAGE_NAME="Data TRANSFORMATION"
    if get_execuationflow.data_transformation_flow==True:
        logging.info(f">>>>>>>>>>>>>>> Starting {STAGE_NAME} pipeline")
        Get_data_transformationpipeline=DataTransformationPipeline()
        Get_data_transformationpipeline.main()
        logging.info("<<<< Application Ended >>>>")
        
    STAGE_NAME="DATA MODEL"
    if get_execuationflow.model_trainer_flow==True:
        logging.info(f">>>>>>>>>>>>>>> Starting {STAGE_NAME} pipeline")
        Get_data_modelpipeline=DataModelPipeline()
        Get_data_modelpipeline.main()
        logging.info("<<<< Application Ended >>>>")
    else:
        logging.info(f"-------------- Stage {STAGE_NAME} is skipped.")
    logging.info(f"Time taken to execute the application is {time.time()-start} seconds")
except Exception as e:
    logging.exception(e)
#----------------------------------------------------------------