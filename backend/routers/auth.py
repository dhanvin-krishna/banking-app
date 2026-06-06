from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.users import User, UserRole
from schemas.user import UserCreate,UserResponse
from utils.security import hash_password

router = APIRouter(prefix="/auth",tags=["Authentication"])

@router.post("/register",response_model=UserResponse,status_code=201)

def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="Email already registered")


    hashed = hash_password(user_data.password)

    new_user = User(
        full_name = user_data.full_name,
        email = user_data.email,
        hashed_password = hashed,
        role = UserRole[user_data.role.value]
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
    
