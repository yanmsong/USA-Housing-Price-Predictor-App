import logging
import os
import config.config as conf

import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("create_database")

Base = declarative_base()


class Price_Prediction(Base):
    """Create a data model for the database to be set up for capturing housing features"""

    __tablename__ = 'housing'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    region = Column(String(100), unique=False, nullable=False)
    type = Column(String(100), unique=False, nullable=False)
    sqfeet = Column(Integer, unique=False, nullable=False)
    beds = Column(Integer, unique=False, nullable=False)
    baths = Column(Integer, unique=False, nullable=False)
    comes_furnished = Column(Integer, unique=False, nullable=False)
    parking_options = Column(String(100), unique=False, nullable=False)
    predicted_price = Column(Integer, unique=False, nullable=False)

    def __repr__(self):
        housing_repr = "<Price_Prediction(id='%s', region='%s', type='%s', sqfeet='%s', beds='%s', \
                        baths='%s', comes_furnished='%s', parking_options='%s', predicted_price='%s')>"
        return housing_repr % (self.id, self.region, self.type, self.sqfeet, self.beds, self.baths, 
                               self.comes_furnished, self.parking_options, self.predicted_price)


def get_engine_string(RDS):
    """Get the engine string for RDS, get the path of sqlite database schema if RDS=False
    Args:
        RDS (boolean): Default is False.
            If False: create the database schema locally in sqlite
            If True: create the database schema in RDS
    Return:
        engine_string (str): Path to store database schema if RDS=False; An engine string if RDS=True
    """

    if RDS:
        logging.info('Creating database in RDS.')
        conn_type = "mysql+pymysql"
        user = os.environ.get("MYSQL_USER")
        password = os.environ.get("MYSQL_PASSWORD")
        host = os.environ.get("MYSQL_HOST")
        port = os.environ.get("MYSQL_PORT")
        database = os.environ.get("DATABASE_NAME")
        engine_string = "{}://{}:{}@{}:{}/{}".format(conn_type, user, password, host, port, database)

        return  engine_string
  
    else:
        logging.info('Creating database locally.')
        return conf.SQLITE


def create_db():
    """Create a database with the data models inherited from `Base` (Price_Prediction)"""

    logger.info("RDS: %s" % conf.RDS)

    # create engine
    engine = sql.create_engine(get_engine_string(conf.RDS))

    # create database
    Base.metadata.create_all(engine)

    logging.info("Database created")




