import pickle
import pytest
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

from src.classification.classifier import DocumentClassifier
from src.classification.models.logistic_regression import LogisticalRegressionModel
from src.file_processing.readers import get_text_from_file


@pytest.fixture(name="artefact_path")
def artefact_path_fixture():
    return Path(__file__).parent.resolve() / "artefacts"


@pytest.fixture(name="model")
def model_fixture(artefact_path):
    model_path = artefact_path / "sample_model.pkl"
    with open(model_path, "rb") as handle:
        return pickle.load(handle)


@pytest.fixture(name="sample_file", params=["bank_statements.pdf", "driving_licenses.jpg", "invoice_receipts.jpg", "invoices.pdf", "passports.png"])
def sample_file_fixture(request, artefact_path):
    filename = request.param
    file = artefact_path / "documents" / filename
    file_stream = BytesIO(file.read_bytes())
    text = get_text_from_file(filename, file_stream)
    yield file.stem, text


@pytest.fixture(name="classifier")
def classifier_fixture(artefact_path):
    test_model_path = artefact_path / "sample_model.pkl"
    return DocumentClassifier.initialise(LogisticalRegressionModel, test_model_path)
