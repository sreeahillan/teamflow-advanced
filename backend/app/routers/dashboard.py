from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from sqlalchemy import select,func
from app.database import get_db
from app.models import Task,Project,Activity,User
from app.security import current_user
router=APIRouter(prefix="/api/dashboard",tags=["Dashboard"])
@router.get("")
def dashboard(db:Session=Depends(get_db),user:User=Depends(current_user)):
    tq=select(Task)
    if user.role=="team_member": tq=tq.where(Task.assignee_id==user.id)
    tasks=db.scalars(tq).all()
    pq=select(Project)
    if user.role=="team_member": pq=pq.where(Project.members.any(id=user.id))
    projects=db.scalars(pq).all()
    aq=select(Activity).order_by(Activity.created_at.desc()).limit(8)
    if user.role=="team_member": aq=aq.where(Activity.actor_id==user.id)
    activities=db.scalars(aq).all()
    counts={s:sum(t.status==s for t in tasks) for s in ["To Do","In Progress","Review","Completed"]}
    return {"total_projects":len(projects),"total_tasks":len(tasks),"status_counts":counts,
      "completion_percent":round(counts["Completed"]*100/len(tasks)) if tasks else 0,
      "recent_activities":[{"id":a.id,"action":a.action,"detail":a.detail,"actor":a.actor.name,"created_at":a.created_at} for a in activities]}
