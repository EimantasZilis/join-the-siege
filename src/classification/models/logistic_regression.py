import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

from src.classification.models.interface import BaseModel


class LogisticalRegressionModel(BaseModel):
    def __init__(self, dataset: pd.DataFrame, test_fraction: int = 0.2):
        self.dataset = dataset
        self.model = LogisticRegression()
        self.vectoriser = CountVectorizer()

        text_train, text_test, doc_type_train, doc_type_test = train_test_split(
            dataset.text, dataset.doc_type, test_size=test_fraction
        )
        self._test_dataset = {"text": text_test, "doc_type": doc_type_test}
        self._train_dataset = {"text": text_train, "doc_type": doc_type_train}

    def train(self) -> None:
        print("Starting model training...")
        self.vectoriser.fit(self._train_dataset["text"])
        vectorised_train = self.vectoriser.transform(self._train_dataset["text"])
        self.model.fit(vectorised_train, self._train_dataset["doc_type"])

        accuracy = self.score_accuracy()
        print(f"Model trained with {accuracy*100}% accuracy")

    def predict(self, text: str) -> str:
        vectorised_text = self.vectoriser.transform([text])
        return list(self.model.predict(vectorised_text))[0]

    def score_accuracy(self) -> float:
        vectorised_test = self.vectoriser.transform(self._test_dataset["text"])
        return self.model.score(vectorised_test, self._test_dataset["doc_type"])
