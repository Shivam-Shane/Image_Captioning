import logging
import os
from datetime import datetime

logger=logging.getLogger("ImageCaptioning")

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H')}.log" #What type of log name to use
LOGS_PATH = os.path.join(os.getcwd(), "LOGS", LOG_FILE)       
os.makedirs(LOGS_PATH, exist_ok=True)
LOG_FILE_PATH = os.path.join(LOGS_PATH, LOG_FILE) # where to save log files

logging.basicConfig(
            filename=LOG_FILE_PATH,
            format="[%(asctime)s %(lineno)s] %(levelname)s %(message)s ",
            level=logging.DEBUG,
            )