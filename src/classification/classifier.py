from __future__ import annotations

from src.classification.models.interface import BaseModel
from src.constants import MAX_TRAINING_DOCS_PER_DOC_TYPE, SAMPLE_DATASET_PICKLE_DIR
from src.helpers import load_pkl_file, save_pkl_file
from src.training_data.parser import read_and_parse_sample_files


MODEL_FILE =  f"model_{MAX_TRAINING_DOCS_PER_DOC_TYPE}_docs_per_doctype.pkl"
MODEL_FILEPATH = SAMPLE_DATASET_PICKLE_DIR / MODEL_FILE


class DocumentClassifier:
    def __init__(self, model) -> None:
        self.model = model

    @classmethod
    def initialise(cls, model_class: BaseModel) -> DocumentClassifier:
        """Initialises document classifier and trains the model.

        The model is cached for speed as a pkl file.
        """
        if MODEL_FILEPATH.exists():
            trained_model = load_pkl_file(MODEL_FILEPATH)
            return cls(trained_model)
        
        training_dataframe = read_and_parse_sample_files()
        model = model_class(training_dataframe)
        model.train()

        save_pkl_file(MODEL_FILEPATH, model)
        return cls(model)
    
    def predict(self, text: str) -> str:
        """Predicts document type based on document text"""
        return self.model.predict(text)
