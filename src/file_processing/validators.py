from pathlib import Path
from werkzeug.datastructures import FileStorage

from src.file_processing.extensions import SUPPORTED_EXTENSIONS


class InvalidFileError(Exception):
    """A custom exception class for invalid files"""


def validate_file(file: FileStorage) -> None:
    """Validates input file.

    Raises:
        InvalidFileError if the file is invalid or not supported
    """
    if file.filename == "":
        raise InvalidFileError("No selected file")

    if not Path(file.filename).suffix in SUPPORTED_EXTENSIONS:
        raise InvalidFileError("File type not allowed")
