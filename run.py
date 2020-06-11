# For this run.py script, I refer to the class material: https://github.com/MSIA/2020-msia423/tree/master/reproducibility

import pandas as pd
import argparse
import yaml
import logging
import config.flaskconfig as conf

logging.basicConfig(format='%(name)-12s %(levelname)-8s %(message)s', level=logging.DEBUG)
logger = logging.getLogger('USA-Housing-Price-Predictor')
logging.getLogger('botocore').setLevel(logging.ERROR)
logging.getLogger('s3transfer').setLevel(logging.ERROR)
logging.getLogger('urllib3').setLevel(logging.ERROR)


from src.import_data import import_data
from src.clean_data import clean_data
from src.featurize import featurize
from src.train_model import run_train
from src.score_model import run_score
from src.evaluate_model import run_evaluate
from create_db import create_db, Price_Prediction


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Model pipeline.")

    parser.add_argument('--config', default='config/config.yaml', help='Path to configuration file')
    parser.add_argument('--raw_data_path', default='data/housing_raw.csv', help='Path to download raw data from S3 bucket')
    parser.add_argument('--clean_data_path', default='data/clean.csv', help='Path to store data after cleaning')
    parser.add_argument('--features_path', default='data/features.csv', help='Path to store data after featurizing')
    parser.add_argument('--model_path', default='models/model.pkl', help='Path to store model object')
    parser.add_argument('--data_path_prefix', default='models/data', help='Prefix of path for saving training and test features and targets')
    parser.add_argument('--score_path', default='models/scores.csv', help='Path to store model scores')
    parser.add_argument('--performance_path', default='models/performance.csv', help='Path to store model performance result')

    args = parser.parse_args()

    # load configuration file
    with open(args.config, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        logger.info("Configuration file loaded from %s" % args.config)

    # pull data from S3 bucket
    import_data(config['import']['bucket'], config['import']['s3_file'], args.raw_data_path)

    # clean data
    input = pd.read_csv(args.raw_data_path)
    logger.info('Input data loaded from %s', args.raw_data_path)
    output = clean_data(input, **config['clean'])
    output.to_csv(args.clean_data_path, index=False)
    logger.info("Output csv saved to %s" % args.clean_data_path)

    # generate features
    input = pd.read_csv(args.clean_data_path)
    logger.info('Input data loaded from %s', args.clean_data_path)
    output = featurize(input, **config['featurize'])
    output.to_csv(args.features_path, index=False)
    logger.info("Output csv saved to %s" % args.features_path)

    # train model
    input = pd.read_csv(args.features_path)
    logger.info('Input data loaded from %s', args.features_path)
    run_train(input, args.model_path, args.data_path_prefix, **config['train'])

    # score model
    input = pd.read_csv('%s-test.csv' % args.data_path_prefix)
    logger.info('Input data loaded from %s-test.csv', args.data_path_prefix)
    run_score(input, args.model_path, args.score_path, **config['score'])

    # evaluate model
    input = pd.read_csv(args.score_path)
    logger.info('Input data loaded from %s', args.score_path)
    run_evaluate(input, args.performance_path, **config['evaluate'])



