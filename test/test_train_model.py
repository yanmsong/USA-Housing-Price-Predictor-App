import numpy as np
import pandas as pd
import os
import pickle
import pytest
import sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

from src.train_model import train, data_split

def test_data_split_good():
	"""Good path unit test for the functionality of data_split"""
	df_true = pd.read_csv("test/sample_data.csv")
	df_test = df_true.copy()
	target = df_true['price']
	features = df_true.loc[:, df_true.columns != 'price']

	X_train_true, X_test_true, y_train_true, y_test_true = train_test_split(features, target, 
															test_size=0.4, random_state=0)

	split_data = {'test_size': 0.4, 'random_state': 0}
	X_train_test, X_test_test, y_train_test, y_test_test = data_split(df_test, 'price', split_data)

	assert X_train_true.equals(X_train_test)
	assert y_train_true.equals(y_train_test)
	assert X_test_true.equals(X_test_test)
	assert y_test_true.equals(y_test_test)	


def test_data_split_bad():
	"""Bad path unit test for the functionality of data_split"""
	df = pd.read_csv("test/sample_data.csv")
	split_data = {'test_size': 0.4, 'random_state': 0}

	with pytest.raises(KeyError) as e:
		X_train, X_test, y_train, y_test = data_split(df, 'orange', split_data)

	assert str(e.value) == "'Target column does not exist!'"


def test_train_model_type_good():
	"""Good path unit test for the functionality of train"""
	df = pd.read_csv("test/sample_features.csv")

	y_train = df['price']
	X_train = df.loc[:, df.columns != 'price']

	params = {'n_estimators': 5, 'random_state': 2}
	rf_test = train(X_train, y_train, params)

	# test model type
	test_model_type = str(type(rf_test))
	true_model_type = "<class 'sklearn.ensemble._forest.RandomForestRegressor'>"
	assert test_model_type == true_model_type


def test_train_model_attributes_good():
	"""Good path unit test for the functionality of train"""
	df = pd.read_csv("test/sample_features.csv")

	y_train = df['price']
	X_train = df.loc[:, df.columns != 'price']

	params = {'n_estimators': 5, 'random_state': 2}
	rf_test = train(X_train, y_train, params)

	# test model attributes
	assert rf_test.get_params()['n_estimators'] == 5
	assert rf_test.get_params()['random_state'] == 2


def test_train_bad():
	"""Bad path unit test for the functionality of train"""
	df = pd.read_csv("test/sample_features.csv")
	df['test'] = 'test'

	y_train = df['price']
	X_train = df.loc[:, df.columns != 'price']

	params = {'n_estimators': 5, 'random_state': 2}

	with pytest.raises(ValueError) as e:
		rf_test = train(X_train, y_train, params)

	assert str(e.value) == 'Wrong data type of inputs for training a random forest regression model!'

