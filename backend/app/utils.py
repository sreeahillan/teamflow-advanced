from app.models import Activity
def log(db, actor, action, detail, project_id=None, task_id=None):
    db.add(Activity(actor_id=actor.id,action=action,detail=detail,project_id=project_id,task_id=task_id))
