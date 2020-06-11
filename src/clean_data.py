import numpy as np
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def clean_data(df, cols_to_drop, cols_to_use):
	"""Data cleaning

	Args:
		df (`pd.DataFrame`): dataframe of the raw dataset
		cols_to_drop (`list` of `str`): useless columns to drop
		cols_to_use (`list` of `str`): columns to use for the next step
		
	Returns:
		df (`pd.DataFrame`): new dataframe after cleaning
	"""

	logger.info("Begin to clean data.")

	if not all(col in df.columns for col in cols_to_drop):
		raise KeyError('Column to drop does not exist!')

	if not all(col in df.columns for col in cols_to_use):
		raise KeyError('Column to use does not exist!')

	# drop useless columns
	df = df.drop(cols_to_drop, axis='columns')
	logger.debug("Columns dropped: %s", cols_to_drop)

	try:
		# remove rows with outliers: price beyond $5000, square footage beyond 4000 feet, 
		# and beyond 3 standard deviations of the mean for beds and baths.
		# note that 99th quantile of price is 3395 and 99th quantile of sqfeet is 2405
		df_new = df[df.price <= 5000]
		df_new = df_new[df_new.sqfeet <= 4000]
		logger.debug("Rows with price beyond $5,000 are removed.")
		logger.debug("Rows with sqfeet beyond 4,000 are removed.")

		df_new = df_new[np.abs(df_new.beds-df_new.beds.mean()) <= (3*df_new.beds.std())]
		df_new = df_new[np.abs(df_new.baths-df_new.baths.mean()) <= (3*df_new.baths.std())]
		logger.debug("Rows with beds or baths beyond 3 standard deviations of its mean are removed.")

		df = df_new

		# drop two rare housing types: land and assisted living
		df = df[df.type!='land']
		df = df[df.type!='assisted living']
		logger.debug("Rows for `land` or `assisted living` housing types are removed.")

		# drop rows with laundry_options being null
		df = df[df.laundry_options.notnull()]
		logger.debug("Rows with `laundry_options` being null are removed.")

	except AttributeError:
		logger.error("Dataframe has no required attribute")

	except Exception as e:
		logger.error(e)

	df = df[cols_to_use]
	logger.debug("Columns remained: %s", cols_to_use)

	logger.info("Data cleaning completed.")

	return df




