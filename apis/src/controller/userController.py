
import json

from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Body, Depends

from src.auth.auth_bearer import JWTBearer
from src.auth.auth_handler import sign_jwt

from src.schemas.userSchema import UserLoginModel

router = APIRouter()

from src.adapter.vpc_create import CreateVPC
from src.adapter.get_vpc import GetVPC

from src.adapter import test_boto
from src.config import boto_config
from src.auth import auth_handler

@router.post("/login", tags=["USER"])
async def user_login(
    request: Request,
    form: UserLoginModel = Depends(),
):
    if check_user(form):
        return auth_handler.sign_jwt(form.user_email)
    
    return_data = {
        "status":False,
        "message": "Not a valid user!!", 
        "data":{}
    }
    
    return JSONResponse(content=jsonable_encoder(return_data), status_code=401)

def check_user(form):

    if ( form.user_email.strip() == boto_config.USER_EMAIL and
        form.password == boto_config.USER_PASSWORD ):
    
        print("Valid user")
        return True

    return False
        