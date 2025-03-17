import boto3
from botocore.config import Config

# from vpc_create import CreateVPC
# from get_vpc import GetVPC
# ##import boto3
from src.config import boto_config

def test_boto_aws():
    try:
        session = boto3.Session(
            aws_access_key_id=boto_config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=boto_config.AWS_SECRETE_ACCESS_KEY,
        )


        ## for testing 
        s3 = session.resource('s3')
        # Output the bucket names
        print('Existing buckets:')
        for bucket in s3.buckets.all():
            print(bucket.name)

        return True
    except Exception as e:
        print("Error in aws-boto initilaization session", e)
        return False

def get_boto3_session(region):
    try:
        session = boto3.Session(
            aws_access_key_id=boto_config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=boto_config.AWS_SECRETE_ACCESS_KEY,
            region_name=region
        )
        return session
    except Exception as e:
        print("Error in aws-boto initilaization session", e)
        return False
##CreateVPC()
##GetVPC()