import numpy as np
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def clean_data(df, cols_to_drop, cols_to_use):
	"""Data cleaning

	Args:
		df: dataframe of the raw dataset
		cols_to_drop: useless columns to drop
		cols_to_use: columns to use for the next step
		
	Returns:
		A new dataframe after cleaning
	"""

	logger.info("Begin to clean data.")

	# drop useless columns
	df = df.drop(cols_to_drop, axis='columns')

	# remove rows with outliers: price beyond $5000, square footage beyond 4000 feet, 
	# and beyond 3 standard deviations of the mean for beds and baths.
	# note that 99th quantile of price is 3395 and 99th quantile of sqfeet is 2405

	df_new = df[df.price <= 5000]
	df_new = df_new[df_new.sqfeet <= 4000]

	df_new = df_new[np.abs(df_new.beds-df_new.beds.mean()) <= (3*df_new.beds.std())]
	df_new = df_new[np.abs(df_new.baths-df_new.baths.mean()) <= (3*df_new.baths.std())]

	df = df_new

	# drop two rare housing types: land and assisted living
	df = df[df.type!='land']
	df = df[df.type!='assisted living']

	# drop rows with laundry_options being null
	df = df[df.laundry_options.notnull()]

	df = df[cols_to_use]

	logger.info("Data cleaning completed.")

	return df




