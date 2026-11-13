import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import auth,users,projects,tasks,dashboard
logging.basicConfig(level=logging.INFO,format="%(asctime)s %(levelname)s %(name)s %(message)s")
app=FastAPI(title="TeamFlow API",version="1.0.0",description="Project and team management API")
app.add_middleware(CORSMiddleware,allow_origins=[settings.FRONTEND_ORIGIN],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
for r in [auth.router,users.router,projects.router,tasks.router,dashboard.router]: app.include_router(r)
@app.get("/")
def root(): return {"message":"TeamFlow API is running","docs":"/docs"}
