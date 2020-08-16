# USA Housing Price Predictor App

<!-- toc -->

- [Project Charter](#project-charter)
- [Directory structure](#directory-structure)
- [Running the model pipeline in Docker](#running-the-model-pipeline-in-docker)
  * [1. Build the image](#1-build-the-image)
  * [2. Run the container for model pipeline](#2-run-the-container-for-model-pipeline)
  * [3. Run the container for unit tests](#3-run-the-container-for-unit-tests)
  * [Optional step](#optional-step)
    + [Run the container for uploading data to S3 bucket](#run-the-container-for-uploading-data-to-s3-bucket)
    + [Run the container for creating database schema](#run-the-container-for-creating-database-schema)
- [Running the app in Docker](#running-the-app-in-docker)
  * [0. Configure Flask app](#0-configure-flask-app)
  * [1. Build the image](#1-build-the-image)
  * [2. Run the container for the Flask app](#2-run-the-container-for-the-flask-app)
  * [3. Kill and remove the container](#3-kill-and-remove-the-container)
- [Remove artifacts](#remove-artifacts)

<!-- tocstop -->
## Project charter

### Vision: 
Housing price information online is kind of scattered. It takes lots of time and effort to collect such information and then analyze them to evaluate the price of a specific house that fits users’ needs, especially when it comes to the US states as a whole instead of isolated urban housing markets. 

This project is born in order to: 1) enable potential homebuyers to efficiently find the up-to-date countrywide housing price information based on their preferences, 2) help house sellers better understand the housing market before setting the price.

### Mission: 
Predict housing price using supervised machine learning models based on Kaggle’s “USA Housing Listings” data that scrapped from Craigslist (the world’s largest collection of privately sold housing options) in Jan. 2020. 

The web app will enable users to input their preferences on housing features and get an estimated price in several seconds. 

Data source: https://www.kaggle.com/austinreese/usa-housing-listings

### Success criteria:
* Machine Learning performance metric:  

  Given the range of the housing price (rent per month) in the data is approximately from $500 to $2,000, the best predictive model should achieve Root Mean Square Error (RMSE) less than $200. From the perspective of homebuyers, a difference of $200 (per month) between the predicted price and the truth is reasonable/acceptable and thus the app would be considered as useful.
  
  To further investigate the model performance for different populations, the RMSE for different types of housing (apartment vs. house vs. condo etc.) or the RMSE for different states in US will be evaluated. 

* Business outcome metric:

  Those users who have visited the web app to predict housing price will be contacted later asking for their experience. The satisfaction rate should be greater than 70%.


## Directory structure 

```
├── README.md                         <- You are here
├── app
│   ├── static/                       <- CSS, JS files that remain static
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── boot.sh                       <- Start up script for launching app in Docker container.
│   ├── Dockerfile                    <- Dockerfile for building image to run app  
│
├── config                            <- Directory for configuration files 
│   ├── logging/                      <- Configuration of python loggers
│   ├── config.yaml                   <- Configurations for model pipeline
│   ├── flaskconfig.py                <- Configurations for Flask API 
│
├── data                              <- Folder that contains data used or generated as well as database if created locally
│
├── deliverables/                     <- Any white papers, presentations, final work products that are presented or delivered to a stakeholder 
│   ├── 423Presentation.pdf           <- Final presentation slides
│
├── models/                           <- Trained model objects (TMOs), model predictions, and/or model summaries
│
├── src/                              <- Source code for the project 
│   ├── import_data.py                <- Script for downloading data from s3 bucket
│   ├── clean_data.py                 <- Script for data cleaning
│   ├── featurize.py                  <- Script for feature engineering
│   ├── train_model.py                <- Script for training model
│   ├── score_model.py                <- Script for scoring model
│   ├── evaluate_model.py             <- Script for evaluating model performance
│
├── test/                             <- Files necessary for running unit tests
│   ├── test_clean_data.py            <- Script for unit test on clean_data module 
│   ├── test_featurize.py             <- Script for unit test on featurize module
│   ├── test_train_model.py           <- Script for unit test on train_model module
│   ├── test_score_model.py           <- Script for unit test on score_model module
│   ├── test_evaluate_model.py        <- Script for unit test on evaluate_model module
│   ├── sample_data.csv               <- Sample data of the raw dataset (the first 10 rows) for unit tests
│   ├── sample_features.csv           <- Sample data of features.csv (20 rows and 6 columns) for unit tests
│
├── app.py                            <- Flask wrapper for running the model 
├── run.py                            <- Simplifies the execution of one or more of the src scripts
├── upload_data.py                    <- Script for uploading data to target s3 bucket
├── create_db.py                      <- Script for creating database (locally in sqlite or in RDS)
├── Dockerfile                        <- Dockerfile for building image to run model pipeline  
├── Makefile                          <- Makefile for uploading data to S3 bucket, creating database, and running model pipeline  
├── requirements.txt                  <- Python package dependencies 
```

## Running the model pipeline in Docker

Note: You have to be on the Northwestern VPN.

### 1. Build the image

The Dockerfile for running the model pipeline is in this directory (the root of the repo). To build the Docker image, run from this directory:

```bash
docker build -t housing .
```

This command builds the Docker image, with the tag `housing`

### 2. Run the container for model pipeline

To run the container that will execute the whole model pipeline (start from downloading raw data from S3 bucket), first export AWS credentials:

```bash
export AWS_ACCESS_KEY_ID=<your AWS_ACCESS_KEY_ID>
export AWS_SECRET_ACCESS_KEY=<your AWS_SECRET_ACCESS_KEY>
```

then run from this directory: 

```bash
docker run \
-e AWS_ACCESS_KEY_ID \
-e AWS_SECRET_ACCESS_KEY \
--mount type=bind,source="$(pwd)",target=/app/ housing pipeline 
```

Note: the csv file is ~500 MB, so downloading it from S3 bucket takes a while, and training the random forest model also takes a while because 100 trees are used, so please be patient. 

File paths for the location the artifacts are loaded from and saved to are configurable. There are in total 8 file paths for the model pipeline: CONFIG_PATH (path to configuration file), RAW_DATA_PATH (path to download raw data from S3 bucket), CLEAN_DATA_PATH (path to store data after cleaning), FEATURES_PATH (path to store data after featurizing), MODEL_PATH (path to store model object), DATA_PATH_PREFIX (prefix of path for saving training and test features and targets), SCORE_PATH (path to store model scores), and PERFORMANCE_PATH (path to store model performance result). The following command is using the default file paths, which has the same effect as the command above. You can change them based on your needs. 

```bash
docker run \
-e AWS_ACCESS_KEY_ID \
-e AWS_SECRET_ACCESS_KEY \
--mount type=bind,source="$(pwd)",target=/app/ housing pipeline \
CONFIG_PATH=config/config.yaml \
RAW_DATA_PATH=data/housing_raw.csv \
CLEAN_DATA_PATH=data/clean.csv \
FEATURES_PATH=data/features.csv \
MODEL_PATH=models/model.pkl \
DATA_PATH_PREFIX=models/data \
SCORE_PATH=models/scores.csv \
PERFORMANCE_PATH=models/performance.csv
```

### 3. Run the container for unit tests

To run unit tests for each function, including "good path" and "bad path", run from this directory:

```bash
docker run --mount type=bind,source="$(pwd)",target=/app/ housing unit_tests
```

### Optional step

#### Run the container for uploading data to S3 bucket

You should first download the dataset (a csv file) manually from https://www.kaggle.com/austinreese/usa-housing-listings
Just sign in if you have a Kaggle account already, otherwise please register one and then sign in. After sign in, click `download`. 

Once finishing downloading, please unzip the csv file. The name would be `housing.csv`.

Then to run the container that will upload data to S3 bucket, run from this directory:
```bash
docker run \
-e AWS_ACCESS_KEY_ID \
-e AWS_SECRET_ACCESS_KEY \
housing upload
```

Note: due to the size of data, please be patient when uploading.

Similar to the second step, here LOCAL_FILE_PATH (path for local file to upload), BUCKET_NAME (S3 bucket name), and S3_FILE_PATH (S3 path for file to be uploaded) are all configurable. The default values are given as below, and you can change them based on your needs. 

```bash
docker run \
-e AWS_ACCESS_KEY_ID \
-e AWS_SECRET_ACCESS_KEY \
housing upload \
LOCAL_FILE_PATH=data/housing.csv \
BUCKET_NAME=nw-yanmengsong-s3 \
S3_FILE_PATH=housing.csv
```

#### Run the container for creating database schema

Database schema could be created either locally in sqlite or in RDS. You could change `SQLALCHEMY_DATABASE_URI` below to do so. First export `SQLALCHEMY_DATABASE_URI`:

```bash
export SQLALCHEMY_DATABASE_URI=<your connection string>
```
then run from this directory:

```bash
docker run -e SQLALCHEMY_DATABASE_URI --mount type=bind,source="$(pwd)",target=/app/ housing create_database 
```

## Running the app in Docker

### 0. Configure Flask app 

`config/flaskconfig.py` holds the configurations for the Flask app. It includes the following configurations:

```python
DEBUG = True  # Keep True for debugging, change to False when moving to production 
LOGGING_CONFIG = "config/logging/local.conf"  # Path to file that configures Python logger
HOST = "0.0.0.0" # the host that is running the app. 0.0.0.0 when running locally 
PORT = 5000  # What port to expose app on. Must be the same as the port exposed in app/Dockerfile 
APP_NAME = "USA-Housing-Price-Predictor"
SQLALCHEMY_TRACK_MODIFICATIONS = True 
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100 # Limits the number of rows returned from the database 
```

### 1. Build the image

The Dockerfile for running the flask app is in the `app/` folder. To build the image, run from this directory (the root of the repo): 

```bash
docker build -f app/Dockerfile -t webapp .
```

This command builds the Docker image, with the tag `webapp`

### 2. Run the container for the Flask app

To run the app, run from this directory:

```bash
docker run \
-e SQLALCHEMY_DATABASE_URI \
--mount type=bind,source="$(pwd)",target=/app/ \
-p 5000:5000 --name test webapp
```

You should now be able to access the app at http://0.0.0.0:5000/ in your browser. 

This command runs the `webapp` image as a container named `test` and forwards the port 5000 from container to your laptop so that you can access the flask app exposed through that port. 

If `PORT` in `config/flaskconfig.py` is changed, this port should be changed accordingly (as should the `EXPOSE 5000` line in `app/Dockerfile`)

Note: The web app writes to a table, and you could change `SQLALCHEMY_DATABASE_URI` in the command to either write to local database or to your RDS. You should create database schema first (instruction is provided in `Optional step-Run the container for creating database schema`.

### 3. Kill and remove the container 

Once finished with the app, you will need to kill and remove the container. To do so: 

```bash
docker kill test 
docker rm test
```

where `test` is the name given in the `docker run` command.

## Remove artifacts 

```bash
docker run --mount type=bind,source="$(pwd)",target=/app/ housing clean
```
