# Heron Coding Challenge - File Classifier

## Getting Started
1. Clone the repository:
```shell
git clone <repository_url>
cd heron_classifier
```

2. Install dependencies:
```shell
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

You will also need to install tesseract for the OCR to work. For Ubuntu, run:
```shell
sudo apt install tesseract-ocr
sudo apt install libtesseract-dev
```
Alternativaly, please see https://tesseract-ocr.github.io/tessdoc/Installation.html
for more information.

3. Download sample_data
This repo is using sample data source from https://www.kaggle.com/datasets. 
Rather than bloating the repo, they need to be downloaded by running:
```shell
python -m src.training_data.downloader
```
It will download sample_data and put it under `sample_data` folder. This should
only be run once.

4. Run the Flask app:
When running the app for the very first time, it will take longer to run,
because it will have to read the training dataset, OCR it, parse the data 
and train the model. Once it is complete, it will cache the ML model as a
.pkl file to improve the performance when restarting the app in the future.

```shell
python -m src.app
```

5. Test the classifier using a tool like curl:
```shell
curl -X POST -F 'file=@path_to_pdf.pdf' http://127.0.0.1:5000/classify_file
```

6. Run tests:
```shell
pytest
```
## How it works
There are a few steps to this repo:
1. Download sample_data from kaggle.
2. Start the app. When it is run for the first time, it will read, OCR and pre-process sample_data
into a dataframe and train the ML model using linear regression. This is only done once for speed
as the model is cached. 

## Configuration
Currently the app is configured to use 30 documents for training for each document type. 
This is done for speed and performance reasons. Since there are more sample docs available,
we can increase this limit by amending `MAX_TRAINING_DOCS_PER_DOC_TYPE` variable in `src/constants`. 

By changing this value, the app will reprocess the sample_data, train and cache the new ML model
when it is next started.

## Limitations and future improvements
### Licenses
For the purposes of this exercise, the licensing requirements for packages and sample datasets
were ignored. This means that for a real production use-case, any non-compliant package for 
production use case should be replaced with equivalent packages.

### Model training
There are two slow steps when starting the app:
 - Pre-processing the data including OCRing
 - Model training

In the production use case, both of these steps should be separated into a
separate step, especially when dealing with bigger training datasets. To mitigate
this for the purposes of this exercise, the ML model is cached. 

### ML Model limitations
Current model will always try to classify a model into one of the document types. In other
words, it will not be able to tell if you if the document doesn't fit into any of the 
pre-defined document types. More work is needed or to be able to say that a document
could not be classified. Alternatively, a completely different model is required altogether.

### Loggers
Rather than relying on `print` to display user messages, they should be replaced
with python's `logging` module.

### Tests
I haven't written many tests due to time-limitations. A lot more tests are
needed for a sufficient test-coverage.

### Limited filetype support
Currently, only images, txt and pdf file types are supported. This should be extended
to support a higher range of files.

### Scaling to new industries
I have not had time to adapt the app to be able to handle multiple industries. 

### Concurrency
Classification/extraction jobs can be costly and the app would need to be able to handle
some concurrency. To do this, I consider converting this app to use a production server
(such as gunicorn) to be able to handle concurrent requests. I would also consider making
requests to be asynchronous through celery, so that extraction jobs would block other requests.  