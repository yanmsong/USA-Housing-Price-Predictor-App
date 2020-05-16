from src.upload_data import upload_data
from src.create_db import create_db, Price_Prediction


if __name__ == '__main__':

    # put data into S3 bucket
    upload_data()
    # create database schema
    create_db()
