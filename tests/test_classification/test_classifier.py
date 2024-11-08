def test_classification_predict(classifier, sample_file):
    expected_document_type, text = sample_file
    text_classification = classifier.predict(text)
    assert expected_document_type == text_classification
