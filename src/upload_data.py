import logging
import boto3
import config.config as conf

s3 = boto3.client("s3")

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("upload_data")


def upload_data():
    """Upload data to target S3 bucket"""

    # the local file path, S3 bucket name, and S3 file are all configurable
    local_file = conf.LOCAL_FILE
    bucket = conf.BUCKET_NAME
    s3_file = conf.S3_FILE


    try:
        s3.upload_file(local_file, bucket, s3_file)
        logger.info("Data uploaded to S3 bucket")

    except FileNotFoundError:
        logger.error("The local file was not found")

    except Exception as e:
        logger.error(e)



 