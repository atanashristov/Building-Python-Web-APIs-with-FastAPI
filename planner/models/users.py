# models/users.py: This file will contain the model definition for user operations.

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from models.events import Event


class UserSignUp(BaseModel):
    email: EmailStr
    password: str
    username: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "fastapi@packt.com",
                    "password": "strong!!!",
                    "username": "FastPack",
                }
            ]
        }
    }


class UserSignIn(BaseModel):
    email: EmailStr
    password: str
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "fastapi@packt.com",
                    "username": "strong!!!",
                }
            ]
        }
    }
