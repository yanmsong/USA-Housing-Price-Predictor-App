import logging
import argparse
import boto3

logging.basicConfig(format='%(name)-12s %(levelname)-8s %(message)s', level=logging.INFO)
logger = logging.getLogger('Upload-data')

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


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Upload data to S3 bucket.")

    # user input
    parser.add_argument("--local_file", default='data/housing.csv', help="path for local file to upload")
    parser.add_argument("--bucket", default='nw-yanmengsong-s3', help="S3 bucket name")
    parser.add_argument("--s3_file", default='housing.csv', help="S3 path for file to be uploaded")

    args = parser.parse_args()

    # upload data to S3 bucket
    upload_data(args.local_file, args.bucket, args.s3_file)



 