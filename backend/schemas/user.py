from pydantic import BaseModel, EmailStr
from enum import Enum as PyEnum

class UserRole(str,PyEnum):
    customer = "customer"
    staff = "staff"
    admin = "admin"

class UserCreate(BaseModel):
    full_name : str
    email : EmailStr
    password : str
    role : UserRole = UserRole.customer


class UserResponse(BaseModel):
    id: int
    full_name : str
    email : EmailStr
    role : UserRole
    

    class Config:
        from_attributes = True
        

    
    

   
    