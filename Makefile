.PHONY: all clean

##### upload data to S3 bucket #####
upload: 
	python3 run.py upload --config=config/config.yaml 

##### create database schema #####
create_database:
	python3 run.py database

##### model pipeline #####
data/housing_raw.csv: config/config.yaml 
	python3 run.py import --config=config/config.yaml 

data/clean.csv: data/housing_raw.csv config/config.yaml 
	python3 run.py clean --input=data/housing_raw.csv --config=config/config.yaml --output=data/clean.csv

data/features.csv: data/clean.csv config/config.yaml 
	python3 run.py featurize --input=data/clean.csv --config=config/config.yaml --output=data/features.csv

model/model.pkl: data/features.csv config/config.yaml 
	python3 run.py train --input=data/features.csv --config=config/config.yaml 

model/result.csv: data/features.csv config/config.yaml
	python3 run.py evaluate --input=data/features.csv --config=config/config.yaml

clean:
	rm data/housing_raw

all: data/housing_raw.csv data/clean.csv data/features.csv model/model.pkl model/result.csv
