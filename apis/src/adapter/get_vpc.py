import boto3

from src.config import boto_config

class GetVPC():

    def __init__(self,  **kwargs) -> None:
        super().__init__(**kwargs)
        self.vpc = ""
        self.internetgateway = ""
        self.routetable = ""

        # # create VPC
        # # 1. create VPC
        # self.get_vpc_by_name( boto_config.VPC_REGION, boto_config.VPC)
        # vpc_id = "vpc-019abd9cd24efc188"
        # self.get_vpc_by_id(boto_config.VPC_REGION, vpc_id)

    def get_boto3_session(self, region):
        try:
            session = boto3.Session(
                aws_access_key_id="AKIAR3HUOKM5V7XTCAQR",
                aws_secret_access_key="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",
                region_name=region
            )
            return session
        except Exception as e:
            print("Error in aws-boto initilaization session", e)
            return False
        
    def get_vpc_by_name(self, region, vpc_name):
        """ to get vpc from aws - if exists """
        try:
            boto3_session = self.get_boto3_session(region)
            ec2_client = boto3_session.client('ec2')
            print("initiliazed ec2 client::", ec2_client)

            response = ec2_client.describe_vpcs(
            Filters=[
                        {
                            'Name': 'tag:Name',
                            'Values': [
                                vpc_name,
                            ]
                        },
                    
                ]
            )
            resp = response['Vpcs']
            if resp:
                print(resp)
                return resp
            else:
                print('No vpcs found')
                return False

        except Exception as e:
            print("Error::", e)
            return False
        
    def get_vpc_by_id(self, region, vpc_id):
        """ to get vpc from aws - if exists """
        try: 
            boto3_session = self.get_boto3_session(region)
            ec2_client = boto3_session.client('ec2')
            print("initiliazed ec2 client::", ec2_client)

            response = ec2_client.describe_vpcs(
            VpcIds=[
                    vpc_id,
                ]
            )

            resp = response['Vpcs']
            if resp:
                print(resp)
                return resp
            else:
                print('No vpcs found')
                return False
        except Exception as e:
            print("Error::", e)
            return False

       
    
