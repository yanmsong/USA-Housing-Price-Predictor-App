import pandas as pd
import pickle
import os
import logging

logger = logging.getLogger(__name__)


def score(df, tmo, label):
	"""Score the trained model

	Args:
		df (`pd.DataFrame`): data containing features
		tmo (`sklearn.ensemble._forest.RandomForestRegressor`): trained model object
		label (`str`): target column

	Returns:
		df (`pd.DataFrame`): dataframe containing features and predicted target values
	"""

	if str(type(tmo)) != "<class 'sklearn.ensemble._forest.RandomForestRegressor'>":
		raise TypeError('Wrong model type!')

	X_test = df.loc[:, df.columns != label]
	
	# predict on test data
	y_pred = tmo.predict(X_test)
	df['predict'] = y_pred

	return df


def run_score(df, tmo_path, score_path, label):
	"""Function pulling together all the functionality for model scoring step

	Args:
		df (`pd.DataFrame`): data containing features
		tmo_path (`str`): path to load the trained model object
		score_path (`str`): path to store model scores
		label (`str`): target column

	Returns:
		None
	"""

	try:
		# load the model
		with open(tmo_path, 'rb') as f:
			tmo = pickle.load(f)
	except OSError:
		logger.error("Cannot open %s", tmo_path)
	except Exception as e:
		logger.error(e)

	logger.info("Scoring the trained model...")

	data = score(df, tmo, label)

	# write score results
	data.to_csv(score_path, index=False)
	logger.info('Model scoring results saved to %s', score_path)


