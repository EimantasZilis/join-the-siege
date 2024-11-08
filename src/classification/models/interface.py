from abc import ABC, abstractmethod


class BaseModel(ABC):
    @abstractmethod
    def train(self) -> None:
        pass

    @abstractmethod
    def predict(self, text: str) -> str:
        pass
