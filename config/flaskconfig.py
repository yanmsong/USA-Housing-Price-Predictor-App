import os
DEBUG = True
LOGGING_CONFIG = "config/logging/local.conf"
PORT = 5000
APP_NAME = "USA-Housing-Price-Predictor"
SQLALCHEMY_TRACK_MODIFICATIONS = True
HOST = "0.0.0.0"
# SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
# MAX_ROWS_SHOW = 100

# Connection string
DB_DIALECT = "mysql+pymysql"
DB_USER = os.environ.get("MYSQL_USER")
DB_PW = os.environ.get("MYSQL_PASSWORD")
DB_HOST = os.environ.get("MYSQL_HOST")
DB_PORT = os.environ.get("MYSQL_PORT")
DATABASE = os.environ.get("DATABASE_NAME")
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

# model object
SAVE_TMO_PATH = 'model/model.pkl'

# local: export SQLALCHEMY_DATABASE_URI='sqlite:///data/housing.db'
# rds: export SQLALCHEMY_DATABASE_URI='{DB_DIALECT}://{DB_USER}:{DB_PW}@{DB_HOST}:{DB_PORT}/{DATABASE}'

if SQLALCHEMY_DATABASE_URI is not None:
    pass
elif DB_HOST is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data/housing.db'
else:
    SQLALCHEMY_DATABASE_URI = '{dialect}://{user}:{pw}@{host}:{port}/{db}'.format(dialect=DB_DIALECT, user=DB_USER,
                                                                                  pw=DB_PW, host=DB_HOST, port=DB_PORT,
                                                                                  db=DATABASE)





