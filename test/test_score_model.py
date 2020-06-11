import numpy as np
import pandas as pd
import pytest
import pickle
import sklearn
from sklearn.linear_model import LogisticRegression

from src.score_model import score
from src.train_model import train

def test_score_good():
	"""Good path unit test for the functionality of score"""
	df = pd.read_csv("test/sample_features.csv")

	y_train = df['price']
	X_train = df.loc[:, df.columns != 'price']

	params = {'n_estimators': 3, 'random_state': 2}
	rf = train(X_train, y_train, params)

	y_pred = rf.predict(X_train)
	df['predict'] = y_pred

	df_test = pd.read_csv("test/sample_features.csv")
	df_test = score(df_test, rf, 'price')

	assert df_test.equals(df)


def test_score_bad():
	"""Bad path unit test for the functionality of score"""
	df = pd.read_csv("test/sample_features.csv")

	clf = LogisticRegression()

	with pytest.raises(TypeError) as e:
		df = score(df, clf, 'price')

	assert str(e.value) == 'Wrong model type!'

