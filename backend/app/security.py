from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db
from app.models import User
pwd=CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth=OAuth2PasswordBearer(tokenUrl="/api/auth/login")
def hash_password(p): return pwd.hash(p)
def verify_password(p,h): return pwd.verify(p,h)
def make_token(user_id):
    exp=datetime.now(timezone.utc)+timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"sub":str(user_id),"exp":exp},settings.SECRET_KEY,algorithm="HS256")
def current_user(token:str=Depends(oauth), db:Session=Depends(get_db)):
    error=HTTPException(status_code=401,detail="Invalid or expired token",headers={"WWW-Authenticate":"Bearer"})
    try: uid=int(jwt.decode(token,settings.SECRET_KEY,algorithms=["HS256"])["sub"])
    except (JWTError,ValueError,KeyError): raise error
    user=db.get(User,uid)
    if not user or not user.is_active: raise error
    return user
def require_roles(*roles):
    def check(user:User=Depends(current_user)):
        if user.role not in roles: raise HTTPException(403,"Insufficient permissions")
        return user
    return check
