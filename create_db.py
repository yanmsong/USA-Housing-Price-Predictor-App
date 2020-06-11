import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData, Float
from sqlalchemy.orm import sessionmaker
import logging
import config.flaskconfig as conf

logging.basicConfig(format='%(name)-12s %(levelname)-8s %(message)s', level=logging.INFO)
logger = logging.getLogger('Create-database-schema')

Base = declarative_base()


class Price_Prediction(Base):
    """Create a data model for the database to be set up for capturing housing features"""

    __tablename__ = 'housing'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    state = Column(String(100), unique=False, nullable=False)
    region = Column(Integer, unique=False, nullable=False)
    housing_type = Column(String(100), unique=False, nullable=False)
    sqfeet = Column(Integer, unique=False, nullable=False)
    beds = Column(Integer, unique=False, nullable=False)
    baths = Column(Float, unique=False, nullable=False)
    comes_furnished = Column(Integer, unique=False, nullable=False)
    laundry_options = Column(String(100), unique=False, nullable=False)
    smoking_allowed = Column(Integer, unique=False, nullable=False)
    dogs_allowed = Column(Integer, unique=False, nullable=False)
    wheelchair_access = Column(Integer, unique=False, nullable=False)
    pred_price = Column(Integer, unique=False, nullable=False)

    def __repr__(self):
        housing_repr = "<Price_Prediction(id='%s', state='%s', region='%s', housing_type='%s', sqfeet='%s', \
                        beds='%s', baths='%s', comes_furnished='%s', laundry_options='%s', smoking_allowed='%s',\
                        dogs_allowed='%s', wheelchair_access='%s', pred_price='%s')>"
        return housing_repr % (self.id, self.state, self.region, self.housing_type, self.sqfeet, self.beds, 
                               self.baths, self.comes_furnished, self.laundry_options, self.smoking_allowed, 
                               self.dogs_allowed, self.wheelchair_access ,self.pred_price)


def create_db(engine_string):
    """Create a database with the data models inherited from `Base` (Price_Prediction)

    Args:
        engine_string: url for sqlalchemy database 
        
    Returns:
        None
    """

    logger.info('Setting up MySQL connection')

    # create engine
    engine = sql.create_engine(engine_string)

    # create database
    Base.metadata.create_all(engine)

    if "sqlite" in engine_string:
        logger.info('Database created locally')
    else:
        logger.info('Database created in RDS')


if __name__ == '__main__':

    create_db(conf.SQLALCHEMY_DATABASE_URI)


