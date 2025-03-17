provider "aws" {
  access_key=""
  secret_key=""
  region="us-east-1"
  /* shared_credentials_file = "/mnt/c/users/asheth/projects/test/Other/terraform_deployment/credentials"  
  # Replace with the path to your credentials file
  */
}

## for cognito integration #################################
resource "aws_cognito_user_pool" "pool" {
  name = "api_pool"
}

resource "aws_cognito_user_pool_client" "client_api" {
  name = "client_api"
  allowed_oauth_flows_user_pool_client = true
  generate_secret = false
  allowed_oauth_scopes = ["aws.cognito.signin.user.admin","email", "openid", "profile"]
  allowed_oauth_flows = ["implicit", "code"]
  explicit_auth_flows = ["ADMIN_NO_SRP_AUTH", "USER_PASSWORD_AUTH"]
  supported_identity_providers = ["COGNITO"]
  user_pool_id = aws_cognito_user_pool.pool.id
  callback_urls = ["https://example.com"]
}

## create sample user 
resource "aws_cognito_user" "example" {
  user_pool_id = aws_cognito_user_pool.pool.id
  username = "ankit.s"
  password = "Test@123"
}

## cognito to api-gatweay authentication with our speecifi api 
resource "aws_api_gateway_authorizer" "demo" {
  name = "api_apig_authorizer2"
  rest_api_id = aws_api_gateway_rest_api.hello_world_api.id
  type = "COGNITO_USER_POOLS"
  provider_arns = [aws_cognito_user_pool.pool.arn]
}



################# for IAM and API-Gateway ########################

# IAM role for Lambda
resource "aws_iam_role" "lambda_exec_role" {
  name = "lambda_exec_role"

  assume_role_policy = <<EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": "sts:AssumeRole",
        "Effect": "Allow",
        "Principal": {
          "Service": "lambda.amazonaws.com"
        }
      }
    ]
  }
  EOF
}

# IAM policy for Lambda execution
resource "aws_iam_role_policy" "lambda_exec_policy" {
  role   = aws_iam_role.lambda_exec_role.id
  policy = <<EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        "Resource": "*"
      }
    ]
  }
  EOF
}



# Lambda function
resource "aws_lambda_function" "hello_world" {
  filename         = "lambda.zip"
  function_name    = "hello_world_function"
  role             = aws_iam_role.lambda_exec_role.arn
  handler          = "hello_world.lambda_handler"
  runtime          = "python3.9"

  /* source_code_hash = filebase64sha256("lambda.zip") */
  lifecycle {
    create_before_destroy = true
  }
}

# API Gateway REST API
resource "aws_api_gateway_rest_api" "hello_world_api" {
  name        = "HelloWorldAPI"
  description = "API for Hello World Lambda function"
  lifecycle {
    create_before_destroy = true
  }
}

# API Gateway Resource (Endpoint)
resource "aws_api_gateway_resource" "lambda_resource" {
  rest_api_id = aws_api_gateway_rest_api.hello_world_api.id
  parent_id   = aws_api_gateway_rest_api.hello_world_api.root_resource_id
  path_part   = "hello"
  lifecycle {
    create_before_destroy = true
  }
}

# API Gateway Method (GET request)
resource "aws_api_gateway_method" "get_method" {
  rest_api_id   = aws_api_gateway_rest_api.hello_world_api.id
  resource_id   = aws_api_gateway_resource.lambda_resource.id
  http_method   = "POST"

   //authorization = "NONE" // as applied cognito authorization
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.demo.id

  lifecycle {
    create_before_destroy = true
  }
}

## for response 
resource "aws_api_gateway_method_response" "response_200" {
  rest_api_id = aws_api_gateway_rest_api.hello_world_api.id
  resource_id = aws_api_gateway_resource.lambda_resource.id
  http_method = aws_api_gateway_method.get_method.http_method
  status_code = "200"
}

resource "aws_api_gateway_integration_response" "proxy" {

  rest_api_id = aws_api_gateway_rest_api.hello_world_api.id
  resource_id = aws_api_gateway_resource.lambda_resource.id
  http_method = aws_api_gateway_method.get_method.http_method
  status_code = "200"

  depends_on = [
    aws_api_gateway_method.get_method,
    aws_api_gateway_integration.lambda_integration

  ]
}

# Lambda integration for API Gateway
resource "aws_api_gateway_integration" "lambda_integration" {
  rest_api_id = aws_api_gateway_rest_api.hello_world_api.id
  resource_id = aws_api_gateway_resource.lambda_resource.id
  http_method = aws_api_gateway_method.get_method.http_method
  type        = "AWS"
  integration_http_method = "POST"
  uri         = aws_lambda_function.hello_world.invoke_arn
  lifecycle {
    create_before_destroy = true
  }
}

# Lambda permission to allow API Gateway to invoke the function
resource "aws_lambda_permission" "allow_api_gateway" {
  statement_id  = "AllowExecutionFromApiGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.hello_world.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.hello_world_api.execution_arn}/*/*"
  lifecycle {
    create_before_destroy = true
  }
}

# Deploy API Gateway
resource "aws_api_gateway_deployment" "api_deployment" {
  depends_on = [aws_api_gateway_integration.lambda_integration]
  rest_api_id = aws_api_gateway_rest_api.hello_world_api.id
  /* aws_api_gateway_stage  = "dev" */
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "dev" {
  deployment_id = aws_api_gateway_deployment.api_deployment.id
  rest_api_id   = aws_api_gateway_rest_api.hello_world_api.id
  stage_name    = "dev"
}

# Output API Gateway URL
output "api_url" {
  value = "${aws_api_gateway_deployment.api_deployment.invoke_url}/hello"
}