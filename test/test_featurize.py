import numpy as np
import pandas as pd
import pytest

from src.featurize import featurize, get_dummies


def test_featurize_good():
	"""Good path unit test for the functionality of featurize"""
	df_true = pd.read_csv("test/sample_data.csv")
	df_test = df_true.copy()

	for col in ['laundry_options', 'state']:
		df_true = get_dummies(df_true, col)

	threshold = df_true.price.quantile(.8)
	high_price_region_ls = df_true.groupby('region').filter(lambda x: x.price.mean() > threshold).region.unique().tolist()
	df_true['high_price_region'] = np.where(df_true.region.isin(high_price_region_ls), 1, 0)

	df_true.drop(['region'], inplace=True, axis=1)

	assert df_true.equals(featurize(df_test, ['laundry_options', 'state']))
	

def test_featurize_bad():
	"""Bad path unit test for the functionality of featurize"""
	df = pd.read_csv("test/sample_data.csv")

	with pytest.raises(KeyError) as e:
		df = featurize(df, ['unknown'])

	assert str(e.value) == "'Column does not exist!'"


def test_get_dummies_good():
	"""Good path unit test for the functionality of get_dummies"""
	df_true = pd.read_csv("test/sample_data.csv")
	df_test = df_true.copy()
	type_dummy = pd.get_dummies(df_true['type']).rename(columns=lambda x: 'type_' + str(x))
	df_true = pd.concat([df_true, type_dummy], axis=1)
	df_true.drop(['type'], inplace=True, axis=1)

	assert df_true.equals(get_dummies(df_test, 'type'))
	

def test_get_dummies_bad():
	"""Bad path unit test for the functionality of get_dummies"""
	df = pd.read_csv("test/sample_data.csv")

	df_test = get_dummies(df, 'beds')

	assert df_test.equals(df)

