#  Python App to create VPC in AWS

## User Authentication (for now with static user details, can extend to db)
## Token Validation
## Create VPC in AWS
## Get data back from AWS for vpc details 

### Also create one TERRAFROM Automation APIs (with Api Gateway/Cognito/Authenction/Lambda) API with Hello World API - to showcase just the automation - need to improve here many ways

## Steps to follow :

Pre-Requisite:
In config file : src/config/boto_config.py:
   -- UPDATE below four parameters value:
      AWS_ACCESS_KEY_ID -- 
      AWS_SECRETE_ACCESS_KEY --
      USER_EMAIL --
      USER_PASSWORD --

      Other things if required (Optional):
      VPC_CIDR_BLOCK :

1. To get the Token - Put details in config for USERNAME/Password - Can apply this also in ENV through docker file
2. Start the application as below:
    -- this code is in Dockerfile
    -- Build the image : go in root and execute , have keep 5001 port now, but can chnage or chnage while start the container (by map the host port)
        docker build -t python_app_vpc .
    -- start the container
        docker run -itd -p 5001:5001 python_app_vpc
    -- to view logs of execution
        docker logs -f "CONTAINER_ID"
    
3. Execute the APIs:
    -- 1. To get the User TOKEN
          Method: POST
          http://localhost:5001/api/v1/user/login
          -- form-data : user_name, password: 
          CURL COMMAND: 
          
          curl --location 'localhost:5001/api/v1/user/login' \
        --form 'user_email="USER_EMAIL"' \
        --form 'password="PASSWORD"'

        -- Store the token 
     
     --2. Use that token as Authorization (as Bearer) header in other APIs
          Create VPC:
          Method : POST
          http://localhost:5001/api/v1/vpc/create
          form-data : vpc_name, vpc_region
          HEADER : Authorization: Bearer TOKEN

          curl --location 'localhost:5001/api/v1/vpc/create' \
          --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiVVNFUl9FTUFJTCIsImV4cGlyZXMiOjE3NDIxNzYwNjUuOTA3NTk5Mn0.drOskbBd1yNQc3eW-LeWy9V9-Y9QOyHON55FOI4zCo4' \
          --form 'vpc_name="test"' \
          --form 'vpc_region="us-east-1"'
      
          -- This will create VPC with below details, give back the VPC  ID/Details:
              VPC,
              Internet Gateway,
              Routetable
              Subnets
              Security group for ssh/http : 22/80 ports
          -- Example Output:
              "vpc_name": "test_52182ada-02d3-11f0-8383-0242ac110002",
              "vpc_id": "vpc-078d972b730ed7b1a",
              "vpc_region": "us-east-1",
              "route_id": "rtb-0a6930ec0097ad506",
              "internet_gateway_id": "igw-08084d1ff897f51eb",
              "subnet_id": "subnet-0992f8825e227c2b2"
      
      --3. Get VPC Details:
           Method : GET
           http://localhost:5001/api/v1/vpc/details
           form-data : vpc_id, vpc_region
           HEADER : Authorization: Bearer TOKEN

           curl --location --request GET 'localhost:5001/api/v1/vpc/describe' \
          --header 'allianz-super-secret-key: 123' \
          --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiVVNFUl9FTUFJTCIsImV4cGlyZXMiOjE3NDIxNzYwNjUuOTA3NTk5Mn0.drOskbBd1yNQc3eW-LeWy9V9-Y9QOyHON55FOI4zCo4' \
          --form 'vpc_id="vpc-050f73ed556b553bf"' \
          --form 'vpc_region="us-east-1"'

Note : In above codebase can do many improvements - like code-structure and other things
- Comments (because of time constraints not implemented all)
-- Execution structurte
-- Logging - implemented for testing one logger - can apply everywhere
-- Variables and other things in Secret / ENV or can put in S3 or somewhere and get in login with proper IAM role

=========== 2. Automation Example -- Terraform =================
Note :  Create a terraform file (can create as module, with separate functionalities, because of time constraints - created single file for now)

-- here given example of complete automation with terraform -- this will
   --- Create 
   API GATEWAY
   Cognito USER
   Authorizer (client)  - for Authentication
   Stage
   Lambda - with python - hello world api
   Hello World API - Can replace with our APIs later on 

   -- to just show the end to end automation - with
      terraform init (can replace with S3 bucket later)
      terraform plan
      terraform apply (--auto-approve)
      terraform destroy (--auto-approve)

       

