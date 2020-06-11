LOCAL_FILE_PATH=data/housing.csv
BUCKET_NAME=nw-yanmengsong-s3
S3_FILE_PATH=housing.csv

CONFIG_PATH=config/config.yaml
RAW_DATA_PATH=data/housing_raw.csv
CLEAN_DATA_PATH=data/clean.csv
FEATURES_PATH=data/features.csv
MODEL_PATH=models/model.pkl
DATA_PATH_PREFIX=models/data
SCORE_PATH=models/scores.csv
PERFORMANCE_PATH=models/performance.csv

.PHONY: unit_tests clean

##### upload data to S3 bucket #####
upload: 
	python3 upload_data.py --local_file=${LOCAL_FILE_PATH} --bucket=${BUCKET_NAME} --s3_file=${S3_FILE_PATH}

##### create database schema #####
create_database:
	python3 create_db.py

##### model pipeline #####
pipeline: 
	python3 run.py --config=${CONFIG_PATH} --raw_data_path=${RAW_DATA_PATH} --clean_data_path=${CLEAN_DATA_PATH} \
	--features_path=${FEATURES_PATH} --model_path=${MODEL_PATH} --data_path_prefix=${DATA_PATH_PREFIX} \
	--score_path=${SCORE_PATH} --performance_path=${PERFORMANCE_PATH}

##### unit tests #####
unit_test_clean_data:
	python3 -m pytest test/test_clean_data.py

unit_test_featurize:
	python3 -m pytest test/test_featurize.py

unit_test_train_model:
	python3 -m pytest test/test_train_model.py

unit_test_score_model:
	python3 -m pytest test/test_score_model.py

unit_test_evaluate_model:
	python3 -m pytest test/test_evaluate_model.py

unit_tests: unit_test_clean_data unit_test_featurize unit_test_train_model unit_test_score_model unit_test_evaluate_model

clean:
	rm -f data/*
	rm -f models/*

