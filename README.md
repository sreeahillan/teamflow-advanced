# TeamFlow – Advanced Project & Team Management System

A full-stack assignment implementation using React + Vite, FastAPI, SQLAlchemy, Alembic, PostgreSQL, JWT authentication and role-based access.

## Features
- JWT register/login and hashed passwords
- Roles: `admin`, `project_manager`, `team_member`
- Dashboard counts, task status summary and recent activity
- Project CRUD and project member assignment
- Task CRUD, assignment, priority, status, deadline, search and filters
- Task comments and activity history
- Pagination on task listing
- Swagger API docs at `/docs`
- Environment-based configuration and CORS

## Requirements
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+

## 1. Database
Create a PostgreSQL database:
```bash
sudo -u postgres psql
CREATE DATABASE teamflow_advanced;
CREATE USER teamflow_user WITH PASSWORD 'change_this_password';
GRANT ALL PRIVILEGES ON DATABASE teamflow_advanced TO teamflow_user;
\q
```
If using PostgreSQL 15+, also run:
```bash
sudo -u postgres psql -d teamflow_advanced
GRANT ALL ON SCHEMA public TO teamflow_user;
\q
```

## 2. Backend setup
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```
Edit `backend/.env` and set your PostgreSQL URL and a long random `SECRET_KEY`.

Create tables (simple first-run setup):
```bash
python -m app.init_db
```
Start API:
```bash
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000/docs

**Create the first Admin:** register using `/api/auth/register`; the first registered account is automatically Admin. Later registrations are Team Members. Admins can change roles through the user management endpoint.

## 3. Frontend setup
Open a second terminal:
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```
Open the Vite URL shown (usually http://localhost:5173). Register/login and explore the dashboard.

## 4. Typical demo flow
1. Register the first user (Admin).
2. Register another account (Team Member) in a separate browser/incognito session.
3. Login as Admin and create a project.
4. Add the Team Member to the project.
5. Create tasks, set priorities/deadlines and assign them.
6. Login as Team Member and update task status / add a comment.
7. Show dashboard statistics and activity feed.

## 5. GitHub submission
From the project root:
```bash
git init
git add .
git commit -m "Build TeamFlow project and task management system"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/teamflow-advanced.git
git push -u origin main
```
Do not commit `.env`, `venv/`, `node_modules/`, or secrets. They are excluded by `.gitignore`.

## 6. Submission checklist
- [ ] GitHub repository link
- [ ] Source code pushed
- [ ] README setup instructions
- [ ] `backend/requirements.txt`
- [ ] Database relationship diagram (`docs/ERD.md`)
- [ ] Swagger screenshots or Postman collection (`docs/TeamFlow.postman_collection.json`)
- [ ] Screenshots: dashboard, projects, task list, task details/comments
- [ ] 2–4 minute demo video (record screen + explain workflow)

## Notes
This is a practical starter implementation. Before production deployment, add refresh tokens, rate limiting, email verification, stronger audit policies, automated tests, and production secrets management. The API uses `create_all` for easy local setup; Alembic is configured and an initial migration can be generated with `alembic revision --autogenerate`.
