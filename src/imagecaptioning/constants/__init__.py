from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
CONFIG_FILE_PATH=ROOT_DIR / Path("config/config.yaml") # path to config file, which store configuration code for the project
PARMS_FILE_PATH=ROOT_DIR / Path("/PARMS.YAML")          # path to parms.yaml file, stores model hyper-parameters details.