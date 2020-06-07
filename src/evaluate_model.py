import pandas as pd
import numpy as np
import pickle
import os
import sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import logging

logger = logging.getLogger(__name__)


def evaluate(df, label, split_data, save_tmo_path, save_res_path):
	"""Evaluate the model 

	Args:
		df: the dataframe for modeling
		label: the target column
		split_data: parameters for splitting data
					(test_size: proportion of test data in splitting train/test,
					random_state: seed for splitting data)
		save_tmo_path: location where the model object is saved
		save_res_path: location to save evaluation results

	Returns:
		None
	"""

	logging.info('Evaluating the model...')

	target = df[label]
	features = df.loc[:, df.columns != label]

	# split data into training and test set
	X_train, X_test, y_train, y_test = train_test_split(features, target, 
														test_size=split_data['test_size'],
                                    					random_state=split_data['random_state'])
	# load the model
	rf = pickle.load(open(save_tmo_path, 'rb'))
	
	# predict on test data
	y_pred = rf.predict(X_test)
	mse = mean_squared_error(y_test, y_pred)
	rmse = np.sqrt(mse)

	# write result
	file = open(save_res_path, "w")
	file.write('RMSE on test: %0.3f' % rmse)
	file.close()

	logger.info("Model evaluation results saved to %s", save_res_path)