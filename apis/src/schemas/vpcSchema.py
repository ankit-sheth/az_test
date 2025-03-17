
from fastapi import Form



class VpcCreateModel():
     def __init__(
        self,
        vpc_name: str = Form(...),
        vpc_region: str = Form(...),
     ):
        self.vpc_name = vpc_name
        self.vpc_region = vpc_region

class VpcGetByIdModel():
    def __init__(
        self,
        vpc_id: str = Form(...),
        vpc_region: str = Form(...),
     ):
        self.vpc_id = vpc_id
        self.vpc_region = vpc_region
