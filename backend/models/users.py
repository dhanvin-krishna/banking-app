from sqlalchemy import Column,Integer,String,Enum
from sqlalchemy.sql import func
from sqlalchemy import DateTime
import enum
from database import Base   

class UserRole(enum.Enum):
    customer = "customer"
    staff = "staff"
    admin = "admin"

class User(Base):
    __tablename__ = "users" 

    id = Column(Integer,primary_key=True,index=True)
    full_name = Column(String, nullable=False)
    email = Column(String,unique=True,index=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRole),default=UserRole.customer)
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    