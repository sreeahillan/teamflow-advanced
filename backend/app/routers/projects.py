from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import get_db
from app.models import Project,User,Task,project_members
from app.schemas import ProjectIn,ProjectOut
from app.security import current_user,require_roles
from app.utils import log
router=APIRouter(prefix="/api/projects",tags=["Projects"])
@router.get("",response_model=list[ProjectOut])
def list_projects(search:str|None=None,db:Session=Depends(get_db),user:User=Depends(current_user)):
    q=select(Project).order_by(Project.created_at.desc())
    if user.role=="team_member": q=q.join(project_members).where(project_members.c.user_id==user.id)
    if search: q=q.where(Project.name.ilike(f"%{search}%"))
    return db.scalars(q).unique().all()
@router.post("",response_model=ProjectOut)
def create_project(data:ProjectIn,db:Session=Depends(get_db),user:User=Depends(require_roles("admin","project_manager"))):
    if data.end_date and data.start_date and data.end_date<data.start_date: raise HTTPException(422,"End date must be after start date")
    p=Project(**data.model_dump(),owner_id=user.id); p.members.append(user)
    db.add(p); db.flush(); log(db,user,"Project created",p.name,p.id); db.commit(); db.refresh(p); return p
@router.get("/{pid}")
def project_detail(pid:int,db:Session=Depends(get_db),user:User=Depends(current_user)):
    p=db.get(Project,pid)
    if not p: raise HTTPException(404,"Project not found")
    tasks=db.scalars(select(Task).where(Task.project_id==pid)).all()
    return {"project":ProjectOut.model_validate(p),"members":[{"id":m.id,"name":m.name,"email":m.email} for m in p.members],
            "tasks_total":len(tasks),"completed":sum(t.status=="Completed" for t in tasks)}
@router.put("/{pid}",response_model=ProjectOut)
def update_project(pid:int,data:ProjectIn,db:Session=Depends(get_db),user:User=Depends(require_roles("admin","project_manager"))):
    p=db.get(Project,pid)
    if not p: raise HTTPException(404,"Project not found")
    for k,v in data.model_dump().items(): setattr(p,k,v)
    log(db,user,"Project updated",p.name,p.id); db.commit(); db.refresh(p); return p
@router.delete("/{pid}")
def delete_project(pid:int,db:Session=Depends(get_db),user:User=Depends(require_roles("admin","project_manager"))):
    p=db.get(Project,pid)
    if not p: raise HTTPException(404,"Project not found")
    db.delete(p); db.commit(); return {"message":"Project deleted"}
@router.post("/{pid}/members/{uid}")
def add_member(pid:int,uid:int,db:Session=Depends(get_db),user:User=Depends(require_roles("admin","project_manager"))):
    p=db.get(Project,pid); member=db.get(User,uid)
    if not p or not member: raise HTTPException(404,"Project or user not found")
    if member not in p.members: p.members.append(member)
    log(db,user,"Member assigned",f"{member.name} added to {p.name}",p.id); db.commit(); return {"message":"Member assigned"}
