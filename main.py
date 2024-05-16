# from src.imagecaptioning.components import data_ingestion
import time
from logger import logging
from src.imagecaptioning.pipeline.data_ingestion import DataIngestionPipeline
from src.imagecaptioning.pipeline.data_transformation import DataTransformationPipeline
from executionflow import Executionflow
import warnings
warnings.filterwarnings("ignore")

get_execuationflow=Executionflow()
get_execuationflow=get_execuationflow.get_data_for_executionflow()
try:
    start=time.time()
    logging.info(">>>> Application Started")
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
    else:
        logging.info(f"-------------- Stage {STAGE_NAME} is skipped.")
        logging.info("<<<< Application Ended >>>>")
        logging.info(f"Time taken to execute the application is {time.time()-start} seconds")
except Exception as e:
    logging.exception(e)
    