import numpy as np
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def featurize(df, categorical_cols):
	"""Generate features for modeling

	Args:
		df (`pd.DataFrame`): the dataframe after data cleaning
		
	Returns:
		df (`pd.DataFrame`): new dataframe with newly generated features
	"""

	logger.info("Begin to generate features.")

	if not all(col in df.columns for col in categorical_cols):
		raise KeyError('Column does not exist!')

	# create dummy variables for categorical variables
	for col in categorical_cols:
		df = get_dummies(df, col)

	try:
		# create an indicator feature for high-price region
		# set the threshold to be the 80th quantile of price for all housing listings
		threshold = df.price.quantile(.8)
		high_price_region_ls = df.groupby('region').filter(lambda x: x.price.mean() > threshold).region.unique().tolist()
		df['high_price_region'] = np.where(df.region.isin(high_price_region_ls), 1, 0)

		# drop the original `region` column
		df.drop(['region'], inplace=True, axis=1)
	
	except AttributeError:
		logger.error("Dataframe has no attribute `price`")
	
	except KeyError:
		logger.error("No column called `region`")
	
	except Exception as e:
		logger.error(e)

	logger.info("Feature generation completed.")

	return df


def get_dummies(data, col):
	"""Create dummy variables

	Args:
		data (`pd.DataFrame`): the dataframe to operate on
		col (`str`): the categorical variable from which to create dummy variables
		
	Returns:
		data (`pd.DataFrame`): new dataframe with newly created dummy variables
	"""
	if (data[col].dtype == np.dtype('int64') or data[col].dtype == np.dtype('float64')):
		logger.warning("Cannot create dummy variables because %s is not a categorical variable", col)
		return data

	dummies = pd.get_dummies(data[col]).rename(columns=lambda x: col + '_' + str(x))
	data = pd.concat([data, dummies], axis=1)
	
	# drop the original categorical variable
	data.drop([col], inplace=True, axis=1)
	logger.debug("Dummy variables created for %s", col)

	return data
