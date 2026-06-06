from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.users import User, UserRole
from schemas.user import UserCreate,UserResponse
from utils.security import hash_password
from utils.security import hash_password, verify_password
from utils.jwt import create_access_token
from schemas.user import Userlogin, TokenResponse

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

@router.post("/login",response_model=TokenResponse)
def login(user_data: Userlogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    if not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401,detail="Invalid credentials")

    token = create_access_token(data = {"sub": user.email, "role": user.role.value})

    return TokenResponse(access_token = token , token_type="bearer")
    
