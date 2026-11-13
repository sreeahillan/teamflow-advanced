from sqlalchemy import String, Text, Boolean, Date, DateTime, ForeignKey, Table, Column, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
project_members = Table("project_members", Base.metadata,
    Column("project_id", ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True),
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True))
class User(Base):
    __tablename__="users"
    id: Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str]=mapped_column(String(120))
    email: Mapped[str]=mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str]=mapped_column(String(255))
    role: Mapped[str]=mapped_column(String(30), default="team_member")
    is_active: Mapped[bool]=mapped_column(Boolean, default=True)
    created_at: Mapped[DateTime]=mapped_column(DateTime(timezone=True), server_default=func.now())
    projects: Mapped[list["Project"]]=relationship(secondary=project_members, back_populates="members")
class Project(Base):
    __tablename__="projects"
    id: Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str]=mapped_column(String(180))
    description: Mapped[str|None]=mapped_column(Text, nullable=True)
    start_date: Mapped[Date|None]=mapped_column(Date, nullable=True)
    end_date: Mapped[Date|None]=mapped_column(Date, nullable=True)
    owner_id: Mapped[int]=mapped_column(ForeignKey("users.id"))
    created_at: Mapped[DateTime]=mapped_column(DateTime(timezone=True), server_default=func.now())
    owner: Mapped[User]=relationship()
    members: Mapped[list[User]]=relationship(secondary=project_members, back_populates="projects")
    tasks: Mapped[list["Task"]]=relationship(back_populates="project", cascade="all, delete-orphan")
class Task(Base):
    __tablename__="tasks"
    id: Mapped[int]=mapped_column(primary_key=True)
    title: Mapped[str]=mapped_column(String(180))
    description: Mapped[str|None]=mapped_column(Text, nullable=True)
    status: Mapped[str]=mapped_column(String(30), default="To Do")
    priority: Mapped[str]=mapped_column(String(30), default="Medium")
    due_date: Mapped[Date|None]=mapped_column(Date, nullable=True)
    project_id: Mapped[int]=mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    assignee_id: Mapped[int|None]=mapped_column(ForeignKey("users.id"), nullable=True)
    creator_id: Mapped[int]=mapped_column(ForeignKey("users.id"))
    created_at: Mapped[DateTime]=mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime]=mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    project: Mapped[Project]=relationship(back_populates="tasks")
    assignee: Mapped[User|None]=relationship(foreign_keys=[assignee_id])
    comments: Mapped[list["Comment"]]=relationship(back_populates="task", cascade="all, delete-orphan")
class Comment(Base):
    __tablename__="comments"
    id: Mapped[int]=mapped_column(primary_key=True)
    body: Mapped[str]=mapped_column(Text)
    task_id: Mapped[int]=mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"))
    user_id: Mapped[int]=mapped_column(ForeignKey("users.id"))
    created_at: Mapped[DateTime]=mapped_column(DateTime(timezone=True), server_default=func.now())
    task: Mapped[Task]=relationship(back_populates="comments")
    user: Mapped[User]=relationship()
class Activity(Base):
    __tablename__="activities"
    id: Mapped[int]=mapped_column(primary_key=True)
    action: Mapped[str]=mapped_column(String(100))
    detail: Mapped[str]=mapped_column(Text)
    actor_id: Mapped[int]=mapped_column(ForeignKey("users.id"))
    project_id: Mapped[int|None]=mapped_column(ForeignKey("projects.id", ondelete="SET NULL"), nullable=True)
    task_id: Mapped[int|None]=mapped_column(ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped[DateTime]=mapped_column(DateTime(timezone=True), server_default=func.now())
    actor: Mapped[User]=relationship()
