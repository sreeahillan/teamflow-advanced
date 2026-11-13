from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select,or_
from app.database import get_db
from app.models import Task,Project,User,Comment,Activity
from app.schemas import TaskIn,TaskOut,CommentIn,CommentOut
from app.security import current_user,require_roles
from app.utils import log
router=APIRouter(prefix="/api",tags=["Tasks & Comments"])
STATUSES=["To Do","In Progress","Review","Completed"]; PRIORITIES=["Low","Medium","High","Critical"]
def visible_task(db,tid,user):
    t=db.get(Task,tid)
    if not t: raise HTTPException(404,"Task not found")
    if user.role=="team_member" and t.assignee_id!=user.id: raise HTTPException(403,"Not allowed")
    return t
@router.get("/tasks",response_model=list[TaskOut])
def list_tasks(search:str|None=None,status:str|None=None,priority:str|None=None,project_id:int|None=None,
               page:int=1,page_size:int=10,db:Session=Depends(get_db),user:User=Depends(current_user)):
    page=max(1,page); page_size=min(max(1,page_size),100)
    q=select(Task).order_by(Task.created_at.desc())
    if user.role=="team_member": q=q.where(Task.assignee_id==user.id)
    if search: q=q.where(or_(Task.title.ilike(f"%{search}%"),Task.description.ilike(f"%{search}%")))
    if status: q=q.where(Task.status==status)
    if priority: q=q.where(Task.priority==priority)
    if project_id: q=q.where(Task.project_id==project_id)
    return db.scalars(q.offset((page-1)*page_size).limit(page_size)).all()
@router.post("/tasks",response_model=TaskOut)
def create_task(data:TaskIn,db:Session=Depends(get_db),user:User=Depends(current_user)):
    if data.status not in STATUSES or data.priority not in PRIORITIES: raise HTTPException(422,"Invalid status or priority")
    p=db.get(Project,data.project_id)
    if not p: raise HTTPException(404,"Project not found")
    if data.assignee_id and not db.get(User,data.assignee_id): raise HTTPException(404,"Assignee not found")
    t=Task(**data.model_dump(),creator_id=user.id); db.add(t); db.flush()
    log(db,user,"Task created",t.title,p.id,t.id); db.commit(); db.refresh(t); return t
@router.put("/tasks/{tid}",response_model=TaskOut)
def update_task(tid:int,data:TaskIn,db:Session=Depends(get_db),user:User=Depends(current_user)):
    t=visible_task(db,tid,user)
    if user.role=="team_member":
        t.status=data.status
    else:
        if data.status not in STATUSES or data.priority not in PRIORITIES: raise HTTPException(422,"Invalid status or priority")
        for k,v in data.model_dump().items(): setattr(t,k,v)
    log(db,user,"Task updated",t.title,t.project_id,t.id); db.commit(); db.refresh(t); return t
@router.delete("/tasks/{tid}")
def delete_task(tid:int,db:Session=Depends(get_db),user:User=Depends(require_roles("admin","project_manager"))):
    t=db.get(Task,tid)
    if not t: raise HTTPException(404,"Task not found")
    db.delete(t); db.commit(); return {"message":"Task deleted"}
@router.get("/tasks/{tid}/comments",response_model=list[CommentOut])
def comments(tid:int,db:Session=Depends(get_db),user:User=Depends(current_user)):
    visible_task(db,tid,user)
    return db.scalars(select(Comment).where(Comment.task_id==tid).order_by(Comment.created_at)).all()
@router.post("/tasks/{tid}/comments",response_model=CommentOut)
def add_comment(tid:int,data:CommentIn,db:Session=Depends(get_db),user:User=Depends(current_user)):
    t=visible_task(db,tid,user); c=Comment(body=data.body,task_id=tid,user_id=user.id); db.add(c)
    log(db,user,"Comment added",t.title,t.project_id,t.id); db.commit(); db.refresh(c); return c
