from flask import Flask, Response, request, jsonify
from src.classification.classifier import DocumentClassifier
from src.classification.models.logistic_regression import LogisticalRegressionModel
from src.file_processing.readers import get_text_from_file
from src.file_processing.validators import InvalidFileError, validate_file


app = Flask(__name__)
DOC_CLASSIFICATION = DocumentClassifier.initialise(LogisticalRegressionModel)


@app.route("/classify_file", methods=["POST"])
def classify_file_route() -> tuple[Response, int]:
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]
    try:
        validate_file(file)
    except InvalidFileError as error_msg:
        return jsonify({"error": error_msg.args[0]}), 400

    text = get_text_from_file(file.filename, file.stream)
    classification = DOC_CLASSIFICATION.predict(text)
    return jsonify({"file_class": classification}), 200


if __name__ == "__main__":
    app.run(debug=True)
