import time
from logger import logging
from src.imagecaptioning.pipeline import data_ingestion,data_model,data_transformation
from executionflow import Executionflow
import warnings
warnings.filterwarnings("ignore")

#----------------------------------------------------------------------------------------------
logging.info(">>>> Application Starting.....")
start=time.time()
get_execuationflow=Executionflow()
get_execuationflow=get_execuationflow.get_data_for_executionflow()

try:
    
    STAGE_NAME="DATA INGESTION"
    if get_execuationflow.data_ingestion_flow:
        logging.info(f">>>>>>>>>>>>>>> Starting {STAGE_NAME} pipeline")
        Get_data_ingetsion_pipeline=data_ingestion.DataIngestionPipeline()
        Get_data_ingetsion_pipeline.main()  #calling pipeline.main
        logging.info(f"<<<<<<<<<<<<<<< Stage {STAGE_NAME} is completed successfully")

    STAGE_NAME="Data TRANSFORMATION"
    if get_execuationflow.data_transformation_flow:
        logging.info(f">>>>>>>>>>>>>>> Starting {STAGE_NAME} pipeline")
        Get_data_transformationpipeline=data_transformation.DataTransformationPipeline()
        Get_data_transformationpipeline.main()
        logging.info(f"<<<<<<<<<<<<<<< Stage {STAGE_NAME} is completed successfully")
        
    STAGE_NAME="DATA MODEL"
    if get_execuationflow.model_trainer_flow:
        logging.info(f">>>>>>>>>>>>>>> Starting {STAGE_NAME} pipeline")
        Get_data_modelpipeline=data_model.DataModelPipeline()
        Get_data_modelpipeline.main()
        logging.info(f"<<<<<<<<<<<<<<< Stage {STAGE_NAME} is completed successfully")

    logging.info(f"Application took {time.time()-start} seconds")
except Exception as e:
    logging.error(f"Application took {time.time()-start} seconds")
    logging.exception(e)
#----------------------------------------------------------------------------------------------