from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import status

from functools import wraps

import json

from fastapi import Request

## custom packages
from src.adapter import test_boto
from src.config import boto_config
from src.routes import router
from src.middleware import token_validator

from src.auth.auth_bearer import JWTBearer

## start the app
app = FastAPI(title="ALLIANZ VPC API Docs", version="1.0.0")

## router
app.include_router(router, prefix="/api/v1")


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

    
# Define the OAuth2 password bearer for token authentication
##oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Define a custom middleware for token verification
# class CustomMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request, call_next):
#         try:
#             # Call the verify_access_token function to validate the token
#             token_validator.verify_access_token(request)
#             # If token validation succeeds, continue to the next middleware or route handler
#             response = await call_next(request)
#             return response
#         except HTTPException as exc:
#             # If token validation fails due to HTTPException, return the error response
#             return JSONResponse(content={"detail": exc.detail}, status_code=exc.status_code)
#         except Exception as exc:
#             # If token validation fails due to other exceptions, return a generic error response
#             return JSONResponse(content={"detail": f"Error: {str(exc)}"}, status_code=500)

# # Add the custom middleware to the FastAPI app
# app.add_middleware(CustomMiddleware)

## test route
@app.get('/test', dependencies=[Depends(JWTBearer())])
def test_check_route(request: Request):
    aws_boto_flag = test_boto.test_boto_aws()

    if aws_boto_flag:
        record = {"status":True, "message":"aws setup done", "data":{}}
    else:
        record = {"status":False, "message":"aws setup not done", "data":{"warning":"without this other api not works!!"}}

   
    print(f"VM creation successful: {record}")

    return JSONResponse(content=jsonable_encoder(record), status_code=200)
    

##@ToDo: add logger
@app.exception_handler(RequestValidationError)
def validation_exception_handler(request, exc):
    exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
    print(f'{exc}')
    print(request, exc_str)
    content = {'status_code': 400, 'message': exc_str, 'data': None} ## can be 422 in some condition
    return JSONResponse(content=content, status_code=422)
    #logger.error(request,str(exc))
    #return JSONResponse((str(exc)), status_code=422)