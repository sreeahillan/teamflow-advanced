from datetime import date, datetime
from pydantic import BaseModel, EmailStr, ConfigDict, Field
class RegisterIn(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8)
class LoginIn(BaseModel):
    email: EmailStr
    password: str
class UserOut(BaseModel):
    id:int; name:str; email:EmailStr; role:str; is_active:bool
    model_config=ConfigDict(from_attributes=True)
class TokenOut(BaseModel):
    access_token:str; token_type:str="bearer"; user:UserOut
class ProjectIn(BaseModel):
    name:str=Field(min_length=2,max_length=180); description:str|None=None
    start_date:date|None=None; end_date:date|None=None
class ProjectOut(ProjectIn):
    id:int; owner_id:int; created_at:datetime
    model_config=ConfigDict(from_attributes=True)
class TaskIn(BaseModel):
    title:str=Field(min_length=2,max_length=180); description:str|None=None
    status:str="To Do"; priority:str="Medium"; due_date:date|None=None
    project_id:int; assignee_id:int|None=None
class TaskOut(TaskIn):
    id:int; creator_id:int; created_at:datetime; updated_at:datetime
    model_config=ConfigDict(from_attributes=True)
class CommentIn(BaseModel):
    body:str=Field(min_length=1,max_length=3000)
class CommentOut(BaseModel):
    id:int; body:str; task_id:int; user_id:int; created_at:datetime
    model_config=ConfigDict(from_attributes=True)
