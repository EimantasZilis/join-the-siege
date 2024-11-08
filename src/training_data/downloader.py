import shutil
from pathlib import Path

import kagglehub

from src.classification.enums import DocumentTypes
from src.constants import SAMPLE_DATA_PATH


KAGGLE_DATASETS = {
    DocumentTypes.PASSPORT: {
        "dataset": "trainingdatapro/generated-passports-segmentation",
        "data_folder": "images",
    },
    DocumentTypes.INVOICE_RECEIPT: {
        "dataset": "simranray/invoice-dataset",
        "data_folder": None,
    },
    DocumentTypes.INVOICE: {
        "dataset": "riddhimanghatak/invoice-dataset",
        "data_folder": "invoice_dataset/TestDataSet",
    },
}


class KaggleDataset:
    def __init__(self, name: str, kaggle_dataset: str, data_path: str) -> None:
        self.name = name
        self.dataset = kaggle_dataset
        self.data_path = data_path
        self.output_path = SAMPLE_DATA_PATH / name

    def download(self) -> Path:
        print(f"Downloading sample {self.name} dataset")
        raw_datapath = self._download_dataset()
        self._prepare_output_directory()
        self._move_dataset(raw_datapath)
        self._remove_redundant_files(raw_datapath)

    def _prepare_output_directory(self) -> None:
        if self.output_path.exists():
            print(
                f"{self.output_path} already exists. Removing it before the data is (re)downloaded"
            )
            shutil.rmtree(self.output_path)
        self.output_path.mkdir(parents=True)

    def _download_dataset(self) -> Path:
        return Path(kagglehub.dataset_download(self.dataset, force_download=False))

    def _move_dataset(self, raw_datapath: Path) -> None:
        if self.data_path is None:
            data_path = Path(raw_datapath)
        else:
            data_path = raw_datapath / self.data_path
        data_path.rename(self.output_path)

    def _remove_redundant_files(self, raw_datapath: Path) -> None:
        if self.data_path is not None:
            shutil.rmtree(raw_datapath)


if __name__ == "__main__":
    for name, dataset in KAGGLE_DATASETS.items():
        dataset = KaggleDataset(name.value, dataset["dataset"], dataset["data_folder"])
        dataset.download()
