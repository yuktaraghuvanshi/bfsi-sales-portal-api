# BFSI Sales Portal Backend — Shreed Vyas and Yukta Raghuvanshi

**Project**: BFSI Sales & Lead Portal  
**Assignment**: Assessment Project (AccMoveOn Technologies)  
**Submitted by**: Shreed Vyas and Yukta Raghuvanshi  
**Repo**: https://github.com/yuktaraghuvanshi/bfsi-sales-portal-api.git  
**Assignment Date**: 19-Sep-2025  
**Submission Date**: 26-Sep-2025

---

## 1. Project Overview
Backend for BFSI Sales & Lead Portal, built with FastAPI and PostgreSQL, providing REST APIs for user authentication, customer, product, and lead management, along with dashboard metrics.

---

## 2. Prerequisites
- Python 3.10+  
- PostgreSQL 13+  
- Virtual environment (`venv`)  
- Environment variables (see `.env`)

---

## 3. Environment Variables
Create a `.env` file in `backend/`:

```env
4. Setup & Run
# Step 1: Create virtual environment
python -m venv .venv
.\.venv\Scripts\activate     # Windows
# or source .venv/bin/activate  # Linux / Mac

# Step 2: Install dependencies
pip install -r requirements.txt

# Step 3: Run migrations
alembic upgrade head

# Step 4: Optional - create admin or seed data
python scripts/create_admin.py

# Step 5: Start backend server
python -m uvicorn app.main:app --reload --log-level debug
# Server will run at http://localhost:8000

DATABASE_URL=postgresql://postgres:Yukta.r#250825@localhost/bfsi_db
AUTHJWT_SECRET_KEY=supersecretkey
