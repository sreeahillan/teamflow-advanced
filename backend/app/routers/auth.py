from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.database import get_db
from app.models import User
from app.schemas import RegisterIn, LoginIn, TokenOut, UserOut
from app.security import hash_password, verify_password, make_token, current_user
router=APIRouter(prefix="/api/auth",tags=["Authentication"])
@router.post("/register",response_model=TokenOut)
def register(data:RegisterIn,db:Session=Depends(get_db)):
    if db.scalar(select(User).where(User.email==data.email)): raise HTTPException(409,"Email already registered")
    count=db.scalar(select(func.count(User.id))) or 0
    user=User(name=data.name,email=data.email,hashed_password=hash_password(data.password),role="admin" if count==0 else "team_member")
    db.add(user); db.commit(); db.refresh(user)
    return {"access_token":make_token(user.id),"user":user}
@router.post("/login",response_model=TokenOut)
def login(data:LoginIn,db:Session=Depends(get_db)):
    user=db.scalar(select(User).where(User.email==data.email))
    if not user or not verify_password(data.password,user.hashed_password): raise HTTPException(401,"Incorrect email or password")
    if not user.is_active: raise HTTPException(403,"Account is inactive")
    return {"access_token":make_token(user.id),"user":user}
@router.get("/me",response_model=UserOut)
def me(user:User=Depends(current_user)): return user
