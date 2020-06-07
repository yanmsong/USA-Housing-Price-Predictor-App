import logging
import boto3

logger = logging.getLogger(__name__)

def upload_data(local_file, bucket, s3_file):
    """Upload data to target S3 bucket

    Args:
        local_file: path for local file to upload
        bucket: S3 bucket name
        s3_file: s3 path for file to be uploaded

    Returns:
        None
    """

    s3 = boto3.client("s3")

    try:
        s3.upload_file(local_file, bucket, s3_file)
        logger.info("Data uploaded to S3 bucket")

    except FileNotFoundError:
        logger.error("The local file was not found")

    except Exception as e:
        logger.error(e)




 