# pull data from S3 bucket
python3 run.py import --config=config/config.yaml 

# clean data
python3 run.py clean --input=data/housing_raw.csv --config=config/config.yaml --output=data/clean.csv

# generate features
python3 run.py featurize --input=data/clean.csv --config=config/config.yaml --output=data/features.csv

# train model
python3 run.py train --input=data/features.csv --config=config/config.yaml 

# evaluate model
python3 run.py evaluate --input=data/features.csv --config=config/config.yaml 