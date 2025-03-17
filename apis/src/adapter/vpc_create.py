import boto3

from src.config import boto_config
##from src.adapter import test_boto


class CreateVPC():

    """ to create the vpc """
    """ @ToDo: for lambda access needs to setup the IAM roles/permissions """

    def __init__(self, vpc_name, **kwargs) -> None:
        super().__init__(**kwargs)
        self.vpc = ""
        self.internetgateway = ""
        self.routetable = ""
        self.route = ""
        self.routetable_id = ""
        self.vpc_name = vpc_name
        self.ec2 = None
        self.vpc_id = ""
        self.internetgateway_id = ""
        self.subnet_id = ""


    def get_boto3_session(self, region):
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
    
    def create_vpc_components(self, region):
        try: 
            boto3_session = self.get_boto3_session(region)
            self.ec2 = boto3_session.client('ec2')
            print("initiliazed ec2 client::", self.ec2)

            # create VPC
            # 1. create VPC
            print("# 1. create VPC")
            self.create_vpc()
            
            ## 1.2 - assign name/tag vpc
            print("## 1.2 - assign name/tag vpc")
            self.tag_vpc(self.vpc_name)

            ## 1.3 - public dns zone name for vpc (used for ssh later)
            print("## 1.3 - public dns zone name for vpc (used for ssh later)")
            self.enable_vpc_public_zone()

            ## 2. attach IG- internet gateway
            self.attach_internet_gateway()

            ## 2. create route table
            self.create_route_tables()

            ## 3. create subnets
            self.create_subnets()

            ### 4. associate subnet to route table
            ##self.create_subnet_route_table_associations()
        
            ## 5. create security group
            self.create_security_group_ssh()

            return self

            ## 6. create test vm in this vpc
        except Exception as e:
            print("Error::", e)
            return False

    def create_vpc(self):
        """ create vpc """
        try:
            self.vpc = self.ec2.create_vpc(CidrBlock=boto_config.VPC_CIDR_BLOCK)

            ##self.vpc.wait_until_available()

            print("==vpc===", self.vpc, self.vpc['Vpc']['VpcId'])
            self.vpc_id = self.vpc['Vpc']['VpcId']

            
        except Exception as e:
            print("Error in create vpc", e)
            return False
        
    def tag_vpc(self, vpc_name):
        """ tag/custom name to vpc """
        try:
            self.ec2.create_tags(Resources=[self.vpc_id], Tags=[{'Key': 'Name', 'Value': vpc_name}])

            ##self.ec2.create_tags(Tags=[{"Key": "Name", "Value": vpc_name}])

            ##self.vpc.wait_until_available()
        except Exception as e:
            print("Error in create vpc", e)
            return False

    
    def enable_vpc_public_zone(self):
        """ to enable public dns hostname user for SSH into it later"""
        try:
            self.ec2.modify_vpc_attribute( VpcId = self.vpc_id , EnableDnsSupport = { 'Value': True } )
            self.ec2.modify_vpc_attribute( VpcId = self.vpc_id , EnableDnsHostnames = { 'Value': True } )
        except Exception as e:
            print("Error in create vpc", e)
            return False

    def attach_internet_gateway(self):
        """ create and attach internet gateway to the VPC """
        try:
            internetgateway = self.ec2.create_internet_gateway()
            print("internetgateway::", internetgateway)
            self.internetgateway_id = internetgateway['InternetGateway']['InternetGatewayId']
            self.ec2.attach_internet_gateway(VpcId = self.vpc_id, InternetGatewayId=self.internetgateway_id)
            
            self.internetgateway = internetgateway
        except Exception as e:
            print("Error in create vpc", e)
            return False

    def attach_nat_gateway(self):
        """ Create and attach nat gateway to the VPC """
        try:
            nat_gateway = self.ec2.CfnNatGateway(self, boto_config.NAT_GATEWAY,
                                            allocation_id=self.elastic_ip.attr_allocation_id,
                                            subnet_id=self.subnet_id_to_subnet_map[config.PUBLIC_SUBNET].ref, )
            return nat_gateway
        except Exception as e:
            print("Error in create vpc", e)
            return False

    def create_route_tables(self):
        """ create a route table and a public route """
        try:
            routetable = self.ec2.create_route_table(VpcId = self.vpc_id)
            route = self.ec2.create_route(RouteTableId=routetable['RouteTable']['RouteTableId'], DestinationCidrBlock='0.0.0.0/0', GatewayId=self.internetgateway_id)
            
            self.route = route
            self.routetable_id = routetable['RouteTable']['RouteTableId']
            routetable_data = self.ec2.describe_route_tables(RouteTableIds=[
                routetable['RouteTable']['RouteTableId'],
            ])
            self.routetable =  routetable_data['RouteTables'][0]
        except Exception as e:
            print("Error in create vpc", e)
            return False

    def create_subnets(self):
        """ create subnet and associate it with route table """
        try:
            subnet = self.ec2.create_subnet(CidrBlock=boto_config.VPC_SUBNET_BLOCK, VpcId=self.vpc_id)
            print("====subnet===", subnet)
            self.subnet_id = subnet['Subnet']['SubnetId']

            ##print("====", self.routetable)
            ##self.routetable.associate_with_subnet(SubnetId=self.subnet_id,GatewayId=self.internetgateway_id)
        except Exception as e:
            print("Error in create vpc", e)
            return False
        
    def create_security_group_ssh(self):
        """ create a security group and allow SSH inbound rule through the VPC """
        try:
            securitygroup = self.ec2.create_security_group(GroupName='SSH-ONLY', Description='only allow SSH traffic', VpcId=self.vpc_id)
            print('---securitygroup---',securitygroup)
            security_group_id = securitygroup["GroupId"]
            self.ec2.authorize_security_group_ingress(
                GroupId=security_group_id,
                IpPermissions=[
                        {
                            'IpProtocol': 'tcp',
                            'FromPort': 80,
                            'ToPort': 80,
                            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                        },
                        {
                            'IpProtocol': 'tcp',
                            'FromPort': 22,
                            'ToPort': 22,
                            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                        }
                    ]
                )
        except Exception as e:
            print("Error in create vpc", e)
            return False

# if __name__ == "__main__":
#     obj = CreateVPC("test-1")
#     obj.create_vpc_components()