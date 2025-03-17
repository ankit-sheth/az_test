# token_validation.py
import os
##import jwt
from fastapi import HTTPException
from src.config import boto_config

from src.auth.auth_handler import decode_jwt

# Retrieve the secret key and algorithm from environment variables
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

def verify_custom_key(request):
    print("=headers==",request.headers)
    
    auth_key_passed = request.headers.get('allianz-super-secret-key')
    print("passed key::", auth_key_passed)
    if auth_key_passed == boto_config.allianz_super_secret_key:
        return True
    else:
        print("Key not valid::", auth_key_passed)

    return False

# def verify_token(x_token: str = Header()):
#     if x_token != "allianz-super-secret-token":
#         raise HTTPException(status_code=400, detail="X-Token header invalid")

# Function to verify the access token extracted from the request
def verify_access_token(request):
    # Extract the token from the request
    ##token = verify_custom_key(request)
    
    try:
        # Decode and verify the token using the secret key and algorithm
        # payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # return payload
        auth_key_flag = verify_custom_key(request)

        if auth_key_flag:
            return True
        else:
            raise HTTPException(status_code=401, detail="Token expired")
    except Exception as e:
        # Raise an HTTPException with status code 401 if the token is invalid
        raise HTTPException(status_code=401, detail="Invalid token")

def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decode_jwt(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True

        return isTokenValid