from fastapi import APIRouter

from src.controller.vpcController import router as vpc_router
from src.controller.userController import router as user_router

router = APIRouter()
router.include_router(vpc_router, prefix="/vpc", tags=["VPC"])
router.include_router(user_router, prefix="/user", tags=["USER"])
