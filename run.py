# For this run.py script, I refer to the class material: https://github.com/MSIA/2020-msia423/tree/master/reproducibility

import pandas as pd
import argparse
import yaml
import logging
import config.flaskconfig as conf

from src.upload_data import upload_data
from src.import_data import import_data
from src.clean_data import clean_data
from src.featurize import featurize
from src.train_model import train
from src.evaluate_model import evaluate
from src.create_db import create_db, Price_Prediction

logging.basicConfig(format='%(name)-12s %(levelname)-8s %(message)s', level=logging.INFO)
logger = logging.getLogger('USA-Housing-Price-Predictor')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Model training pipeline.")

    # user input
    parser.add_argument('step', help='Which step to run', 
                        choices=['upload', 'database', 'import', 'clean', 'featurize', 'train', 'evaluate'])
    parser.add_argument('--input', '-i', default=None, help='Path to input data (optional, default = None)')
    parser.add_argument('--config', help='Path to configuration file')
    parser.add_argument('--output', '-o', default=None, help='Path to save output CSV (optional, default = None)')

    args = parser.parse_args()

    # create database schema
    if args.step == 'database':
        print(conf.SQLALCHEMY_DATABASE_URI)
        create_db(conf.SQLALCHEMY_DATABASE_URI)


    # Load configuration file 
    if args.config is not None:
        with open(args.config, "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            logger.info("Configuration file loaded from %s" % args.config)

    # upload data to S3 bucket
    if args.step == 'upload':
        upload_data(**config['upload'])

    ####### MODEL PIPELINE #######

    if args.input is not None:
        input = pd.read_csv(args.input)
        logger.info('Input data loaded from %s', args.input)

    # pull data from S3 bucket
    if args.step == 'import':
        import_data(**config['import'])
    # clean data
    elif args.step == 'clean':
        output = clean_data(input, **config['clean'])
    # generate features
    elif args.step == 'featurize':
        output = featurize(input)
    # train model
    elif args.step == 'train':
        train(input, **config['train'])
    # evaluate model
    elif args.step == 'evaluate':
        evaluate(input, **config['evaluate'])
    # else:
    #     run_tests(args)

    if args.output is not None:
        output.to_csv(args.output, index=False)

        logger.info("Output csv saved to %s" % args.output)



