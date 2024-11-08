from collections import defaultdict
from io import BytesIO

import pandas as pd

from src.classification.enums import DocumentTypes
from src.constants import (
    MAX_TRAINING_DOCS_PER_DOC_TYPE,
    SAMPLE_DATA_PATH,
    SAMPLE_DATASET_PICKLE_DIR,
    SUPPORTED_EXTENSIONS,
)
from src.file_processing.readers import get_text_from_file


DATASET_PATH = (
    SAMPLE_DATASET_PICKLE_DIR / f"dataset_{MAX_TRAINING_DOCS_PER_DOC_TYPE}_docs_per_doctype.pkl"
)


def read_sample_files() -> dict[str, list[str]]:
    """Reads and returns sample datafiles split by document type"""
    SAMPLE_DATASET_PICKLE_DIR.mkdir(exist_ok=True, parents=True)

    data = defaultdict(list)
    for doc_type in DocumentTypes:
        read_doc_type_files(data, doc_type.value)

    return data


def read_doc_type_files(dataset: dict[str, list[str]], doc_type: str) -> None:
    """Populates dataset variable by going through all sample files for a given
    doc_type. It will only process up to MAX_TRAINING_DOCS_PER_DOC_TYPE number 
    of files for a given document type"""

    files_processed = 0
    data_folder_path = SAMPLE_DATA_PATH / doc_type

    if not data_folder_path.exists():
        print(f"sample_data for {doc_type} not downloaded. Skipping this doument type")
        return

    print(f"Reading and processing {doc_type} sample_data...")
    for file in data_folder_path.iterdir():
        if files_processed >= MAX_TRAINING_DOCS_PER_DOC_TYPE:
            break

        text = get_text_from_file(file.name, BytesIO(file.read_bytes()))
        if file.suffix in SUPPORTED_EXTENSIONS:
            dataset["doc_type"].append(doc_type)
            dataset["text"].append(text)
            files_processed += 1


def read_and_parse_sample_files() -> pd.DataFrame:
    """Reads sample files and returns a dataframe
    containing document text and their document type."""
    data = read_sample_files()
    return pd.DataFrame(data)
