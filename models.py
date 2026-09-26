from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel, EmailStr, field_validator
from zxcvbn import zxcvbn
from db import engine

Base = declarative_base()

#SQLalchemy models
class BaseUser(Base):
    __abstract__ = True
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True)


class User(BaseUser):
    __tablename__ = 'users'

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)


#Pydantic models
class CreateUser(BaseModel):
    first_name:str
    last_name:str
    email:EmailStr
    password:str

    @field_validator('password')
    @classmethod
    def check_password_strength(cls, v:str) -> str:
        results = zxcvbn(v)

        if results['score'] < 3:
            feedback = results['feedback']['suggestions']
            msg = feedback[0] if feedback else "La password è troppo debole"
            raise ValueError(msg)

        return v


class UserResponse(BaseModel):
    id:int
    first_name:str
    last_name:str
    email:EmailStr

    class Config:
        from_attributes = True

class UserLogIn(BaseModel):
    email:EmailStr
    password:str

class UserUpdate(BaseModel):
    first_name:str
    last_name:str
    email:EmailStr

class ChangePassword(BaseModel):
    old_password:str
    new_password:str

    @field_validator('new_password')
    @classmethod
    def check_password_strength(cls, v:str) -> str:
        results = zxcvbn(v)

        if results['score'] < 3:
            feedback = results['feedback']['suggestions']
            msg = feedback[0] if feedback else "La password è troppo debole"
            raise ValueError(msg)

        return v



Base.metadata.create_all(engine)
