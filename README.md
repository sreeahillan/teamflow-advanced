# TeamFlow – Project & Team Management System

TeamFlow is a full-stack web application for managing projects, assigning tasks, tracking progress, and organizing team activities in one place.

The application provides a centralized dashboard where users can manage their projects and tasks based on their assigned roles.

## Tech Stack

**Frontend**

- React.js
- Vite
- CSS
- Axios

**Backend**

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- JWT Authentication

**Database**

- PostgreSQL

**Tools**

- Git and GitHub
- Swagger UI
- Alembic

## Features

### Authentication

- User registration and login
- Password hashing
- JWT-based authentication
- Role-based access

### Dashboard

- Overview of projects and tasks
- Task status tracking
- Project statistics

### Project Management

- Create and view projects
- Store project descriptions and details
- Track project progress

### Task Management

- Create and view tasks
- Assign tasks to users
- Set task priorities and due dates
- Track task status

### Team Management

- View registered team members
- Display user roles

### API

- RESTful API built with FastAPI
- Request validation using Pydantic
- Interactive API documentation through Swagger UI

## Project Structure

```text
teamflow_advanced/
│
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── init_db.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── security.py
│   │   └── utils.py
│   │
│   ├── migrations/
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── api.js
│   │   ├── main.jsx
│   │   └── style.css
│   ├── package.json
│   └── .env.example
│
├── docs/
│   └── ERD.md
│
├── .gitignore
└── README.md
```

## Installation and Setup

### Prerequisites

Install the following before starting:

- Python 3.12 or later
- Node.js and npm
- PostgreSQL
- Git

### 1. Clone the repository

```bash
git clone https://github.com/sreeahillan/teamflow-advanced.git
cd teamflow-advanced
```

### 2. Set up the PostgreSQL database

Open PostgreSQL:

```bash
sudo -u postgres psql
```

Create the database and user:

```sql
CREATE DATABASE teamflow_advanced;
CREATE USER teamflow_user WITH PASSWORD 'your_password';

GRANT ALL PRIVILEGES ON DATABASE teamflow_advanced TO teamflow_user;

\c teamflow_advanced

GRANT ALL ON SCHEMA public TO teamflow_user;
ALTER SCHEMA public OWNER TO teamflow_user;

\q
```

Use your own database password in the application configuration.

### 3. Configure the backend

Open a terminal:

```bash
cd backend

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

Create your environment file:

```bash
cp .env.example .env
```

Update the database connection and application settings in `backend/.env`.

Example database URL:

```env
DATABASE_URL=postgresql+psycopg://teamflow_user:your_password@localhost:5432/teamflow_advanced
```

Set a strong, private JWT secret key in your environment configuration.

### 4. Initialize the database

```bash
python -m app.init_db
```

### 5. Start the backend server

```bash
uvicorn app.main:app --reload
```

Backend URL:

http://127.0.0.1:8000

Swagger API documentation:

http://127.0.0.1:8000/docs

### 6. Configure the frontend

Open another terminal:

```bash
cd frontend

npm install
cp .env.example .env
```

Check that the frontend API URL points to your local backend.

### 7. Start the frontend

```bash
npm run dev
```

Open the application:

http://localhost:5173

## API Documentation

FastAPI provides interactive API documentation.

Once the backend is running, visit:

http://127.0.0.1:8000/docs

You can use Swagger UI to inspect and test the available API endpoints.

## Database Design

The database uses PostgreSQL and SQLAlchemy models.

The entity relationship diagram is available here:

`docs/ERD.md`

## Environment Variables

Environment files contain local configuration and should not be committed to GitHub.

The repository includes `.env.example` files as configuration templates.

Create your own `.env` files when setting up the project.

## Future Improvements

- Project member assignment interface
- Task comments and discussion
- Advanced filtering and sorting
- Pagination
- More detailed activity history
- Improved role and permission management
- Automated testing

## Author

**Sree Ahilan**

GitHub: https://github.com/sreeahillan

---

This project was developed as a full-stack application to practice frontend development, backend API development, database integration, and authentication.
