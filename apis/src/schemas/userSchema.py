
from fastapi import Form

class UserLoginModel():
     def __init__(
        self,
        user_email: str = Form(...),
        password: str = Form(...),
     ):
        self.user_email = user_email
        self.password = password
