import pandas as pd
import numpy as np
import pickle
import sklearn
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import logging

logger = logging.getLogger(__name__)

def train(X_train, y_train, best_params):
	"""Train the model 

	Args:
		X_train (`pd.DataFrame`): Features for training dataset
		y_train (`pd.Series`): True target values for training dataset
		best_params (`dict`): parameters for the model 
							(n_estimators (`int`): the number of trees in the forest,
							random_state (`int`): random state to make model reproducible)		

	Returns:
		rf (`sklearn.ensemble._forest.RandomForestRegressor`): trained model object
	"""

	# checks data types of inputs 
	for col in X_train.columns:
		if X_train[col].dtype not in [np.dtype('float64'), np.dtype('int64')]:
			raise ValueError('Wrong data type of inputs for training a random forest regression model!')

	try:
		rf = RandomForestRegressor(n_estimators=best_params['n_estimators'], random_state=best_params['random_state'])
	except KeyError:
		logger.info("Required parameter not found")
	except Exception as e:
		logger.error(e)

	# fit the model
	rf.fit(X_train, y_train)
	logger.info('Trained model object created:\n%s', str(rf))

	return rf


def data_split(df, label, split_data):
	"""Split data into training and test set

	Args:
		df (`pd.DataFrame`): the dataframe for modeling
		label (`str`): the target column
		split_data (`dict`): parameters for splitting data
							(test_size (`float`): proportion of test data in splitting train/test,
							random_state (`int`): random state to make split reproducible)

	Returns:
		X_train (`pd.DataFrame`): Features for training dataset
		y_train (`pd.Series`): True target values for training dataset
		X_test (`pd.DataFrame`): Features for testing dataset
		y_test (`pd.Series`): True target values for testing dataset
	"""

	if label not in df.columns:
		raise KeyError('Target column does not exist!')

	# extract features and target 
	target = df[label]
	features = df.loc[:, df.columns != label]

	try:
		# split data into training and test set
		X_train, X_test, y_train, y_test = train_test_split(features, target, 
															test_size=split_data['test_size'],
	                                    					random_state=split_data['random_state'])
	except KeyError:
		logger.error("Required parameter not found")
	except Exception as e:
		logger.error(e)

	return X_train, X_test, y_train, y_test


def run_train(df, save_tmo_path, data_path_prefix, label, split_data, best_params):
	"""Function pulling together all the functionality for model training step

	Args:
		df (`pd.DataFrame`): the dataframe for modeling
		save_tmo_path (`str`): path to save the model
		data_path_prefix (`str`): Prefix of path for saving training and test features and targets
		label (`str`): the target column
		split_data (`dict`): parameters for splitting data
							(test_size (`float`): proportion of test data in splitting train/test,
							random_state (`int`): random state to make split reproducible)
		best_params (`dict`): parameters for the model 
							(n_estimators (`int`): the number of trees in the forest,
							random_state (`int`): random state to make model reproducible)

	Returns:
		None
	"""

	logger.info("Splitting data...")
	X_train, X_test, y_train, y_test = data_split(df, label, split_data)

	logger.info("Training a random forest regression model...")
	rf = train(X_train, y_train, best_params)

	try:
		# save the model
		with open(save_tmo_path, "wb") as f:
			pickle.dump(rf, f)
			logger.info("Trained model object saved to %s", save_tmo_path)
	except OSError:
		logger.error("Cannot open %s", save_tmo_path)
	except Exception as e:
		logger.error(e)

	X_train[label] = y_train
	X_test[label] = y_test
	X_train.to_csv('%s-train.csv' % data_path_prefix, index=False)
	logger.info('Training dataset saved to %s', '%s-train.csv' % data_path_prefix)

	X_test.to_csv('%s-test.csv' % data_path_prefix, index=False)
	logger.info('Testing dataset saved to %s', '%s-test.csv' % data_path_prefix)		




