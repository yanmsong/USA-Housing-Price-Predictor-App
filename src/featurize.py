import numpy as np
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def featurize(df):
	"""Generate features for modeling

	Args:
		df: the dataframe after data cleaning
		
	Returns:
		A new dataframe with newly generated features
	"""

	logger.info("Begin to generate features.")

	# create dummy variables for categorical variables
	df = get_dummies(df, 'type')
	df = get_dummies(df, 'laundry_options')
	df = get_dummies(df, 'state')

	# create an indicator feature for high-price region
	# set the threshold to be the 80th quantile of price for all housing listings
	threshold = df.price.quantile(.8)
	high_price_region_ls = df.groupby('region').filter(lambda x: x.price.mean() > threshold).region.unique().tolist()
	df['high_price_region'] = np.where(df.region.isin(high_price_region_ls), 1, 0)

	# drop the original `region` column
	df.drop(['region'], inplace=True, axis=1)

	logger.info("Feature generation completed.")

	return df


def get_dummies(data, col):
	"""Create dummy variables

	Args:
		data: the dataframe to operate on
		col: the categorical variable from which to create dummy variables
		
	Returns:
		A new dataframe with newly created dummy variables
	"""

	dummies = pd.get_dummies(data[col]).rename(columns=lambda x: col + '_' + str(x))
	data = pd.concat([data, dummies], axis=1)
	
	# drop the original categorical variable
	data.drop([col], inplace=True, axis=1)

	return data
