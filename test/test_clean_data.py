import numpy as np
import pandas as pd
import pytest

from src.clean_data import clean_data


def test_clean_data_good():
	"""Good path unit test for the functionality of clean_data"""
	cols_to_drop = ['id', 'url', 'region_url']
	cols_to_use = ['price', 'type', 'sqfeet', 'beds', 'baths', 'laundry_options', 'state', 'region']

	df_true = pd.read_csv("test/sample_data.csv")
	df_test = df_true.copy()
	df_true = df_true.drop(cols_to_drop, axis='columns')

	df_true = df_true[df_true.price <= 5000]
	df_true = df_true[df_true.sqfeet <= 4000]
	df_true = df_true[np.abs(df_true.beds-df_true.beds.mean()) <= (3*df_true.beds.std())]
	df_true = df_true[np.abs(df_true.baths-df_true.baths.mean()) <= (3*df_true.baths.std())]
	df_true = df_true[df_true.type!='land']
	df_true = df_true[df_true.type!='assisted living']
	df_true = df_true[df_true.laundry_options.notnull()]

	df_true = df_true[cols_to_use]

	assert df_true.equals(clean_data(df_test, cols_to_drop, cols_to_use))               


def test_clean_data_bad():
	"""Bad path unit test for the functionality of clean_data"""
	df = pd.read_csv("test/sample_data.csv")

	with pytest.raises(KeyError) as e:
		df = clean_data(df, ['apple', 'url'], ['price', 'type', 'sqfeet', 'beds', 'baths', 'laundry_options', 'state'])

	assert str(e.value) == "'Column to drop does not exist!'"


