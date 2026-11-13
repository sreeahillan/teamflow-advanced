from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import get_db
from app.models import User
from app.schemas import UserOut
from app.security import current_user,require_roles
router=APIRouter(prefix="/api/users",tags=["Users"])
@router.get("",response_model=list[UserOut])
def users(db:Session=Depends(get_db),user:User=Depends(current_user)):
    return db.scalars(select(User).order_by(User.name)).all()
@router.patch("/{user_id}/role",response_model=UserOut)
def set_role(user_id:int,role:str,db:Session=Depends(get_db),admin:User=Depends(require_roles("admin"))):
    if role not in ["admin","project_manager","team_member"]: raise HTTPException(422,"Invalid role")
    u=db.get(User,user_id)
    if not u: raise HTTPException(404,"User not found")
    u.role=role; db.commit(); db.refresh(u); return u
@router.patch("/{user_id}/active",response_model=UserOut)
def set_active(user_id:int,active:bool,db:Session=Depends(get_db),admin:User=Depends(require_roles("admin"))):
    u=db.get(User,user_id)
    if not u: raise HTTPException(404,"User not found")
    u.is_active=active; db.commit(); db.refresh(u); return u
