from pathlib import Path

IMAGE_FILE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".tiff")
TEXT_FILE_EXTENSIONS = (".pdf", ".txt")
SUPPORTED_EXTENSIONS = TEXT_FILE_EXTENSIONS + IMAGE_FILE_EXTENSIONS

# When downloading Kaggle datasets as training data, some of them can be big.
# Reading and OCRing can take a lot of time and memory. For this reason, we
# can set a limit of files to load for every document type using
# MAX_TRAINING_DOCS_PER_DOC_TYPE variable.
# In production, we'd want a big dataset to get more accurate models, so this
# would either be removed or set to a large number
MAX_TRAINING_DOCS_PER_DOC_TYPE = 30
SAMPLE_DATASET_PICKLE_DIR = Path(__file__).parent / "training_data" / "datasets"
SAMPLE_DATA_PATH = Path(__file__).parent.parent / "sample_data"
