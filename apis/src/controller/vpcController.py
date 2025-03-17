
import uuid
import datetime
import json

from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from src.schemas.vpcSchema import VpcCreateModel, VpcGetByIdModel

from src.auth.auth_bearer import JWTBearer
router = APIRouter(dependencies=[Depends(JWTBearer())])

from src.adapter.vpc_create import CreateVPC
from src.adapter.get_vpc import GetVPC

from src.adapter import test_boto
from src.services.log_service import CustomLogger

def set_custom_logger(request):
    """to set the custom logger

    Args:
        request (Request): request object
    Returns:
        CustomLogger : object
    """
    try:
        if request.headers and request.headers["request_trace_id"]:
            request_trace_id = request.headers["request_trace_id"]
        else:
            request_trace_id = uuid.uuid4()
    except Exception as e:
        print("request trace id: not found in Request, generating one:")
        request_trace_id = uuid.uuid4()

    request_trace_id = str(request_trace_id)

    custom_logger = CustomLogger(request_trace_id)

    return custom_logger

# API routes
@router.post("/create")
def create_vm(
    request: Request,
    form: VpcCreateModel = Depends(),
):
    custom_logger = set_custom_logger(request)
    
    custom_logger.debug("VPC Controller-Process Create Request")
    custom_logger.debug("Request Data::" + str(vars(form)))
    
    record = None
    try:
        print("here in vpc post request")
        ## initialize boto

        aws_boto_flag = test_boto.test_boto_aws()

        if aws_boto_flag:
            record = {"aws_setup":True}
            vpc_uuid = uuid.uuid1()
            vpc_unique_name = form.vpc_name.strip()+"_"+str(vpc_uuid)
            region = form.vpc_region
            print("vpc name::", vpc_unique_name)
            vpc_obj = CreateVPC(vpc_unique_name)
            result_obj = vpc_obj.create_vpc_components(region)

            return_data = {
                     "status":True,
                      "message": "VPC created successfully", 
                      "data":{
                          "vpc_name":vpc_unique_name,
                          "vpc_id":result_obj.vpc_id,
                          "vpc_region":region,
                          "route_id": result_obj.routetable_id,
                          "internet_gateway_id": result_obj.internetgateway_id,
                          "subnet_id": result_obj.subnet_id
                      }
                    }
            return JSONResponse(content=jsonable_encoder(return_data), status_code=200)
    
        else:
            return_data = {
                     "status":False,
                      "message": "Failure in vpc creation", 
                      "data":{
                          "vpc_name":vpc_unique_name,
                      }
                    }

            return JSONResponse(content=jsonable_encoder(return_data), status_code=422)

    
    except Exception as e:
        ## @ToDo: apply logger
        print("Error ::", e)
        return False
    

@router.get("/describe")
def create_vm(
    request: Request,
    form: VpcGetByIdModel = Depends(),
):
    record = None
    try:
        print("here in vpc get request")
        ## initialize boto

        aws_boto_flag = test_boto.test_boto_aws()

        if aws_boto_flag:
            record = {"aws_setup":True}
            vpc_id = form.vpc_id
            region  = form.vpc_region

            vpc_obj = GetVPC()
            vpc_data = vpc_obj.get_vpc_by_id(region, vpc_id)

            if vpc_data:
                record = {
                        "status":True,
                        "message": "Get VPC data successfully", 
                        "data": vpc_data
                }
            else:
                record = {
                        "status":True,
                        "message": "VPC  data does not exists", 
                        "data": {"vpc_id":vpc_id, "region":region}
                }
            ##resp_data = jsonable_encoder(record)
            ##print(f"VM creation successful: {resp_data}")
            ##return {"message": "VPC created successfully", "data": resp_data}
            return JSONResponse(content=jsonable_encoder(record), status_code=200)
    
        else:
            return_data = {
                     "status":False,
                      "message": "Failure in vpc get data", 
                      "data":{
                          "vpc_id":vpc_id,
                          "region":region
                      }
                    }

            return JSONResponse(content=jsonable_encoder(return_data), status_code=422)

    except Exception as e:
        ## @ToDo: apply logger
        print("Error ::", e)
        return False
    
def handle_exception(error, custom_message="An error occurred"):
    if isinstance(error, IntegrityError):
        detail = str(error.orig)
        status_code = 422 if "ForeignKeyViolation" in detail else 500
    else:
        detail = custom_message
        status_code = 500
    logger.error(f"{custom_message}: {error}")
    print(f"Error: {custom_message}: {error}")
    raise HTTPException(status_code=status_code, detail=detail)