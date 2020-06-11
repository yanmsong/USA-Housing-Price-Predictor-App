import numpy as np
import pandas as pd
import pytest
import sklearn
from sklearn.metrics import mean_squared_error

from src.evaluate_model import calculate_rmse


def test_calculate_rmse_good():
	"""Good path unit test for the functionality of calculate rmse"""

	y_pred = [1, 2, 3, 4]
	y_true = [2, 2.5, 10, 5]
	mse = mean_squared_error(y_true, y_pred)
	rmse_true = np.sqrt(mse)

	assert rmse_true == calculate_rmse(y_pred, y_true)


def test_calculate_rmse_bad():
	"""Bad path unit test for the functionality of calculate rmse"""

	y_pred = [1, 2, 3, 4]
	y_true = [2, 2.5, 5]
	with pytest.raises(ValueError) as e:
		rmse = calculate_rmse(y_pred, y_true)

	assert str(e.value) == 'Two lists have different length!'