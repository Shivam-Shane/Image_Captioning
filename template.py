import os
from pathlib import Path
from logger import logging
from dataclasses import dataclass

@dataclass
class TemplateGenarator():
    project_name="imagecaptioning"
    list_of_files=(
                    ".github/workflow/.gitkeep",
                    f"src/{project_name}/__init__.py",
                    f"src/{project_name}/components/__init__.py",
                    f"src/{project_name}/utils/__init__.py",
                    f"src/{project_name}/utils/common.py",
                    f"src/{project_name}/config/__init__.py",
                    f"src/{project_name}/config/configuration.py",
                    f"src/{project_name}/pipeline/__init__.py",
                    f"src/{project_name}/entity/__init__.py",
                    f"src/{project_name}/constants/__init__.py",
                    "config/config.yaml",
                    "parms.yaml",
                    "app.py",
                    "main.py",
                    "Dockerfile",
                    "requirements.txt",
                    "setup.py",
                    ".gitignore"
                    )
    
    def genarate_file_structure(self):
        logging.info(f">>>> Inside {self.__class__.__name__}.{self.genarate_file_structure.__name__}")
        try:
            for filepath in self.list_of_files:
                filepath=Path(filepath)
                filedir, filename=os.path.split(filepath)

                if filedir != "":
                    os.makedirs(filedir,exist_ok=True)
                    logging.info(f"creating directory {filedir} for the filename {filename}")

                if (not os.path.exists(filepath)) or (os.path.getsize(filepath) ==0):
                    with open(filepath,'w') as f:
                        logging.info(f"creating file {filepath}")
                else:
                    logging.info(f" file {filepath} already exists") 
        except Exception as e:
            logging.error(f"error occurred while creating file {filepath}")
            logging.exception(e)
        

if __name__=='__main__':
     TemplateGenarator().genarate_file_structure()