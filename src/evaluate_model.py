import pandas as pd
import numpy as np
import sklearn
from sklearn.metrics import mean_squared_error
import logging

logger = logging.getLogger(__name__)


def calculate_rmse(y_pred, y_true):
	"""Calculate root mean squared error

	Args:
		y_pred (`list` of `float`): predicted value
		y_true (`list` of `float`): true value

	Returns:
		rmse (`float`): calculated rmse
	"""
	if len(y_pred) != len(y_true):
		raise ValueError('Two lists have different length!')
	
	mse = mean_squared_error(y_true, y_pred)
	rmse = np.sqrt(mse)

	logger.info('RMSE is %0.3f', rmse)

	return rmse


def run_evaluate(df, performance_path, label, metrics):
	"""Function pulling together all the functionality for model evaluation step

	Args:
		df (`pd.DataFrame`): data containing features, target, and predicted value
		performance_path (`str`): path to store performance results
		label (`str`): target column
		metrics (`list` of `str`): metrics to evaluate on 

	Returns:
		None
	"""

	y_pred = df['predict'].values
	y_true = df[label].values

	logging.info('Evaluating the model...')
	if 'rmse' in metrics:
		rmse = calculate_rmse(y_pred, y_true)

	for m in metrics:
		if m not in ['rmse']:
			logger.warning('No code exists to calculate %s', m)

	try:
		# write result
		file = open(performance_path, "w")
		file.write('RMSE on test: %0.3f' % rmse)
		file.close()
	except OSError:
		logger.error("Cannot open %s", performance_path)
	except Exception as e:
		logger.error(e)	

	logger.info("Model evaluation results saved to %s", performance_path)


