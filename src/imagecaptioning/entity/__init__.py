from dataclasses import dataclass
from pathlib import Path

@dataclass
class ExecuationFlowConfig():
    data_ingestion_flow: bool
    data_validation_flow: bool
    data_transformation_flow: bool
    model_trainer_flow: bool
    model_evaluation_flow: bool

@dataclass
class DataIngestionConfig():
    data_path: Path
    data_ingestion_path: Path

@dataclass
class DataTransformationConfig():
    data_path: Path
    data_ingestion_path: Path
    data_transformation_path: Path
    data_transformation_save_features:Path
    data_transformation_save_captions: Path