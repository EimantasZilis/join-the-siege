from pathlib import Path
from PIL import Image
from typing import Optional

import pytesseract
from pypdf import PdfReader
from werkzeug.datastructures import FileStorage

from src.constants import TEXT_FILE_EXTENSIONS, IMAGE_FILE_EXTENSIONS


class ImageFileReader:
    def __init__(self, file: FileStorage) -> None:
        self.file = file

    def ocr_image(self) -> str:
        """OCRs image and returns text from it."""
        image = Image.open(self.file.stream)
        return pytesseract.image_to_string(image)


class TextFileReader:
    def __init__(self, file: FileStorage) -> None:
        self.file = file
        self.filename = Path(file.filename)

    def read(self) -> Optional[str]:
        """
        Reads and returns text from input file.
        Returns None if it cannot be processed.
        It assumes that the file is text-based and can be processed.
        """
        if self.filename.suffix == ".pdf":
            return self._read_pdf()
        elif self.filename.suffix == ".txt":
            return self._read_txt()
        else:
            return None

    def _read_pdf(self) -> str:
        """Reads and returns text from txt file"""
        reader = PdfReader(self.file.stream)
        return "\n".join([page.extract_text() for page in reader.pages])

    def _read_txt(self) -> str:
        """Reads and returns text from txt file"""
        return self.file.stream.read().decode("utf-8")


def get_text_from_file(file: FileStorage) -> Optional[str]:
    """
    Reads input file and returns text.
    If the input file type is not supported, it will return None

    Inputs:
        file (FileStorage): Input file from the request

    Returns:
        Text from the file or None if the file could not be processed.
    """
    filename = Path(file.filename)
    if filename.suffix in IMAGE_FILE_EXTENSIONS:
        image_reader = ImageFileReader(file)
        return image_reader.ocr_image()

    elif filename.suffix in TEXT_FILE_EXTENSIONS:
        file_reader = TextFileReader(file)
        return file_reader.read()

    else:
        return None
