import boto3
import logging

logger = logging.getLogger(__name__)

def import_data(bucket, s3_file, local_file):
	"""Pull the raw data from S3 bucket

	Args:
		bucket: S3 bucket name
		s3_file: s3 path for file to be downloaded 
		local_file: local path to download file
		
	Returns:
		None
	"""

	s3 = boto3.client('s3')
	s3.download_file(bucket, s3_file, local_file)

	logger.info("Raw data downloaded from S3 bucket to %s", local_file)

