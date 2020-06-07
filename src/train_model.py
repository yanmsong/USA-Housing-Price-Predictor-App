import pandas as pd
import numpy as np
import pickle
import sklearn
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import logging

logger = logging.getLogger(__name__)

def train(df, label, split_data, best_params, save_tmo_path):
	"""Train the model 

	Args:
		df: the dataframe for modeling
		label: the target column
		split_data: parameters for splitting data
					(test_size: proportion of test data in splitting train/test,
					random_state: seed for splitting data)
		best_params: parameters for the model 
					(n_estimators: the number of trees in the forest,
					random_state: seed to control randomness)
		save_tmo_path: path to save the model

	Returns:
		None
	"""

	logger.info("Training a random forest regression model...")

	target = df[label]
	features = df.loc[:, df.columns != label]

	# split data into training and test set
	X_train, X_test, y_train, y_test = train_test_split(features, target, 
														test_size=split_data['test_size'],
                                    					random_state=split_data['random_state'])

	# train the model
	rf = RandomForestRegressor(n_estimators=best_params['n_estimators'], random_state=best_params['random_state'])
	rf.fit(X_train, y_train)

	dir = "model"
	if not os.path.exists(dir):
		os.mkdir(dir)

	# save the model
	with open(save_tmo_path, "wb") as f:
		pickle.dump(rf, f)
		logger.info("Trained model object saved to %s", save_tmo_path)


