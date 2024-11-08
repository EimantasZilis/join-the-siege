from pathlib import Path
from typing import Any

import pickle


def save_pkl_file(filepath: Path, data: Any) -> None:
    """Writes data to a .pkl file"""
    with open(filepath, "wb") as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


def load_pkl_file(filepath: Path) -> Any:
    """Reads dataset from a .pkl file"""
    if not filepath.exists():
        raise FileNotFoundError(f"{filepath} does not exist")

    with open(filepath, "rb") as handle:
        return pickle.load(handle)
