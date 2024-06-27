import logging
import os
from datetime import datetime

logger=logging.getLogger("ImageCaptioning") #using named loggers, we can control the logging level for different parts

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H')}.log" #What type of log file name to use
LOGS_PATH = os.path.join(os.getcwd(), "LOGS", LOG_FILE)    # Path where the log will be stored   
os.makedirs(LOGS_PATH, exist_ok=True)                      # Making sure the directory exists
LOG_FILE_PATH = os.path.join(LOGS_PATH, LOG_FILE) # Saving the log file path for log files

logging.basicConfig(
            filename=LOG_FILE_PATH,
            format="[%(asctime)s %(lineno)s] %(levelname)s %(message)s ",
            level=logging.INFO,
            )    # basin config for our logging, we can chanage as per our needs.

#-----Learn At https://docs.python.org/3/howto/logging.html---------