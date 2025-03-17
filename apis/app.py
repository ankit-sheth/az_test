# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
# from fastapi.exceptions import RequestValidationError
# from fastapi import Depends, FastAPI, Header, HTTPException

# # from fastapi import APIRouter, Depends, Request
# # from fastapi.encoders import jsonable_encoder
# # from fastapi.exceptions import HTTPException

# from src.adapter import test_boto

# from src.routes import router
# from src.auth import auth_handler

# app = FastAPI(title="ALLIANZ reservation API Docs", version="1.0.0")

# app.include_router(router, prefix="/api/v1", Depends[(auth_handler.v)])

# origins = ["*"]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# ## test route
# @app.route('/test', methods=['GET'])
# def test_check_route():
#     aws_boto_flag = test_boto.test_boto_aws()

#     if aws_boto_flag:
#         record = {"aws_setup":True}
#     else:
#         record = {"aws_setup":False}

#     ##resp_data = jsonable_encoder(record)
#     print(f"VM creation successful: {record}")
#     return {"message": "AWS Configure Status !!", "data": record}

# if __name__ == "__main__":
#     app.logger("---in dev-app.py file---")
#     app.logger('Info level log')
#     app.logger('Warning level log')
#     app.run(host="0.0.0.0", port=5001, debug=True)

# # ##@ToDo: add logger
# # @app.exception_handler(RequestValidationError)
# # def validation_exception_handler(request, exc):
# #     exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
# #     print(f'{exc}')
# #     print(request, exc_str)
# #     content = {'status_code': 10422, 'message': exc_str, 'data': None}
# #     return JSONResponse(content=content, status_code=422)
# #     #logger.error(request,str(exc))
# #     #return JSONResponse((str(exc)), status_code=422)

# async def verify_key(x_key: str = Header()):
#     if x_key != "allianz-super-secret-key":
#         raise HTTPException(status_code=400, detail="X-Key header invalid")
#     return x_key

# async def verify_token(x_token: str = Header()):
#     if x_token != "allianz-super-secret-token":
#         raise HTTPException(status_code=400, detail="X-Token header invalid")