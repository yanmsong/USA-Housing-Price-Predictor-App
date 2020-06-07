import pandas as pd
import pickle
import os
import sklearn
from sklearn.ensemble import RandomForestRegressor
import logging

logger = logging.getLogger(__name__)


def prediction(input_ls):

	# load the model
	save_tmo_path = 'model/housing.pkl'
	rf = pickle.load(open(save_tmo_path, 'rb'))

	sample = pd.read_csv(user_input)

	pred_price = int(rf.predict(sample))

	return pred_price









	
