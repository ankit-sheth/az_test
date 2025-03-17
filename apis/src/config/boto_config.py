VPC="custom-vpc"
VPC_CIDR_BLOCK="192.168.0.0/16"
VPC_SUBNET_BLOCK="192.168.1.0/24"
NAT_GATEWAY=""
VPC_REGION="us-east-1"
AWS_ACCESS_KEY_ID=""
AWS_SECRETE_ACCESS_KEY=""

USER_EMAIL="USER_EMAIL" ## stored in db - unique
USER_PASSWORD="PASSWORD"  ## stored in db - encrypted - compare the same with user passed and encrypted with salt
USER_PASSWORD_SALT="123allianz#@!"  ## these should be stored in db, for each user separate salt
#allianz_super_secret_key="123"

TOKEN_VALID_TIME = 600

