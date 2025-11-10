# 🏢 Apartment Maintenance Request System
## Complete Installation & Deployment Guide

**Version:** 1.0.0  
**Database:** PostgreSQL (NEON Cloud)  
**Tech Stack:** FastAPI + React + Vite + TailwindCSS

---

## 📋 TABLE OF CONTENTS

1. [Quick Start (5 Minutes)](#quick-start)
2. [Prerequisites](#prerequisites)
3. [Installation Steps](#installation-steps)
4. [Running the Application](#running-the-application)
5. [Database Setup](#database-setup)
6. [Troubleshooting](#troubleshooting)
7. [Project Information](#project-information)
8. [API Documentation](#api-documentation)

---

## 🚀 QUICK START (5 Minutes)

**For demo/presentation - Follow these exact steps:**

### **Step 1: Install Prerequisites**
```bash
# Check if Python 3.12+ is installed
python --version

# Check if Node.js 18+ is installed
node --version
npm --version
```

If not installed, download:
- **Python 3.12:** https://www.python.org/downloads/
- **Node.js 18+:** https://nodejs.org/ (LTS version)

---

### **Step 2: Install Backend Dependencies**
```bash
# Navigate to backend folder
cd backend

# Create virtual environment (optional but recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install all Python packages
pip install -r requirements.txt
```

---

### **Step 3: Install Frontend Dependencies**
```bash
# Navigate to frontend folder (open new terminal)
cd frontend

# Install all Node.js packages
npm install
```

---

### **Step 4: Start Backend Server**
```bash
# In backend folder
cd backend

# Activate venv if not already activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Start FastAPI server
uvicorn app.main:app --reload

# Server will start at: http://127.0.0.1:8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
Connected to PostgreSQL: neondb
INFO:     Application startup complete.
```

---

### **Step 5: Start Frontend Server**
```bash
# In frontend folder (NEW TERMINAL - don't close backend!)
cd frontend

# Start Vite dev server
npm run dev

# Frontend will start at: http://localhost:5173
```

You should see:
```
VITE v5.4.21  ready in 730 ms
➜  Local:   http://localhost:5173/
```

---

### **Step 6: Open Application**

**Open browser and go to:** http://localhost:5173

**You should see:**
- Dashboard with KPI cards (Active Requests, Completed, etc.)
- Charts showing request analytics
- Navigation menu (Dashboard, Buildings, Units, Tenants, Staff, Requests)

**✅ SUCCESS! The application is running!**

---

## 📦 PREREQUISITES

### **Required Software:**

| Software | Minimum Version | Download Link | Purpose |
|----------|----------------|---------------|---------|
| **Python** | 3.12+ | https://www.python.org/downloads/ | Backend API |
| **Node.js** | 18+ LTS | https://nodejs.org/ | Frontend build tool |
| **npm** | 9+ | (Included with Node.js) | Package manager |
| **Git** | Latest | https://git-scm.com/ | Version control (optional) |

### **Operating System:**
- ✅ Windows 10/11
- ✅ macOS 11+
- ✅ Linux (Ubuntu 20.04+)

### **Hardware:**
- **RAM:** Minimum 4GB (8GB recommended)
- **Storage:** 500MB free space
- **Internet:** Required for database connection (NEON Cloud)

### **Database Access:**
- NEON PostgreSQL account (already configured)
- Database credentials provided in `.env` file
- Internet connection required (cloud database)

---

## 🔧 INSTALLATION STEPS

### **Step 1: Extract Project Files**

```bash
# Extract the ZIP file to a location of your choice
# Example: C:\Projects\apartment-maintenance-system
# or ~/Projects/apartment-maintenance-system
```

**Project Structure:**
```
apartment-maintenance-system/
├── backend/              # FastAPI backend
│   ├── app/             # Application code
│   ├── requirements.txt # Python dependencies
│   ├── .env            # Database credentials
│   └── ...
├── frontend/            # React frontend
│   ├── src/            # Source code
│   ├── package.json    # Node.js dependencies
│   └── ...
├── README.md           # This file
└── SETUP_GUIDE.md      # Additional setup info
```

---

### **Step 2: Install Python Dependencies**

```bash
# Navigate to backend folder
cd backend

# Option A: Using virtual environment (RECOMMENDED)
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Option B: Global installation (not recommended)
# Skip virtual environment steps

# Install all dependencies
pip install -r requirements.txt
```

**Expected packages installed:**
- fastapi==0.104.1
- uvicorn[standard]==0.24.0
- sqlalchemy==2.0.23
- asyncpg==0.29.0
- psycopg2-binary==2.9.9
- pydantic==2.5.0
- python-dotenv==1.0.0
- And 8 more packages...

**Installation time:** ~2-3 minutes

---

### **Step 3: Install Node.js Dependencies**

```bash
# Navigate to frontend folder
cd frontend

# Install all dependencies
npm install
```

**Expected packages installed:**
- react ^18.2.0
- react-router-dom ^6.20.0
- axios ^1.6.2
- recharts ^2.10.3
- vite ^5.0.8
- tailwindcss ^3.3.6
- And 20+ more packages...

**Installation time:** ~3-5 minutes

---

### **Step 4: Verify Database Connection**

The `.env` file in the `backend` folder contains database credentials:

```properties
# PostgreSQL Configuration (NEON)
PG_HOST=ep-broad-resonance-ade3fcco-pooler.c-2.us-east-1.aws.neon.tech
PG_DATABASE=neondb
PG_USER=neondb_owner
PG_PASSWORD=npg_SkIJU01uZvKo
PG_SSLMODE=require
PG_PORT=5432
```

**⚠️ IMPORTANT:** These credentials are for the shared NEON PostgreSQL database. You've been added as a collaborator.

**To verify access:**
1. Go to https://console.neon.tech
2. Login with your account
3. You should see the "neondb" database

**Database already contains:**
- 5 buildings (Boston neighborhoods)
- 200 units
- 100 tenants
- 5 staff members
- 200 maintenance requests

**No seeding needed!** The database is ready to use.

---

## ▶️ RUNNING THE APPLICATION

### **Method 1: Using Two Terminals (Recommended for Demo)**

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate  # Windows only
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Then open:** http://localhost:5173

---

### **Method 2: Using Production Build**

**Build frontend:**
```bash
cd frontend
npm run build
# Creates: frontend/dist/ folder
```

**Serve with backend:**
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Note:** For production deployment, you'll need to configure frontend to build to backend's static folder or use a reverse proxy (nginx).

---

### **Method 3: Quick Demo Script (Windows)**

Create `start-demo.bat` in project root:
```batch
@echo off
echo Starting Apartment Maintenance System...
echo.

echo [1/2] Starting Backend...
start cmd /k "cd backend && venv\Scripts\activate && uvicorn app.main:app --reload"

timeout /t 5

echo [2/2] Starting Frontend...
start cmd /k "cd frontend && npm run dev"

timeout /t 5

echo.
echo ===================================
echo Backend:  http://127.0.0.1:8000
echo Frontend: http://localhost:5173
echo ===================================
echo.
echo Opening browser...
timeout /t 3
start http://localhost:5173

echo.
echo Press any key to stop servers...
pause
taskkill /f /im python.exe
taskkill /f /im node.exe
```

**Run:** Double-click `start-demo.bat`

---

## 🗄️ DATABASE SETUP

### **Database is Already Set Up!**

The NEON PostgreSQL database is **already configured and populated** with:

- ✅ 5 tables created (buildings, units, tenants, staff, requests)
- ✅ ENUM types defined (issue_type, priority, status)
- ✅ Foreign key relationships established
- ✅ 510 records seeded

**No additional setup needed!**

---

### **To Re-Initialize Database (Optional - Only if needed):**

```bash
cd backend

# Create tables (if not exists)
python init_db.py

# Seed sample data (if tables are empty)
python seed_pg_data.py
```

**⚠️ WARNING:** Only run seeding if database is empty! Running it again will add duplicate records.

---

### **Database Access:**

**NEON Console:** https://console.neon.tech

**SQL Editor Queries:**
```sql
-- Check record counts
SELECT 'buildings' as table_name, COUNT(*) FROM buildings
UNION ALL
SELECT 'units', COUNT(*) FROM units
UNION ALL
SELECT 'tenants', COUNT(*) FROM tenants
UNION ALL
SELECT 'staff', COUNT(*) FROM staff
UNION ALL
SELECT 'requests', COUNT(*) FROM requests;

-- View recent requests
SELECT external_id, status, priority, issue_type, created_at 
FROM requests 
ORDER BY created_at DESC 
LIMIT 10;
```

---

## 🔧 TROUBLESHOOTING

### **Issue 1: "Python not found"**

**Solution:**
1. Download Python from https://www.python.org/downloads/
2. During installation, check "Add Python to PATH"
3. Restart terminal
4. Verify: `python --version`

---

### **Issue 2: "Node.js not found"**

**Solution:**
1. Download Node.js LTS from https://nodejs.org/
2. Run installer
3. Restart terminal
4. Verify: `node --version` and `npm --version`

---

### **Issue 3: "pip install fails with error"**

**Solution:**
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Try installing again
pip install -r requirements.txt

# If specific package fails, install individually:
pip install fastapi uvicorn sqlalchemy asyncpg psycopg2-binary
```

---

### **Issue 4: "npm install fails"**

**Solution:**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json  # Mac/Linux
rmdir /s /q node_modules  # Windows
del package-lock.json     # Windows

# Install again
npm install
```

---

### **Issue 5: "Backend won't start - Database connection error"**

**Solution:**

Check `.env` file credentials:
```bash
cd backend
cat .env  # Mac/Linux
type .env # Windows
```

Verify:
- ✅ PG_HOST is correct
- ✅ PG_PASSWORD has no extra spaces
- ✅ PG_SSLMODE=require
- ✅ Internet connection active

Test connection:
```bash
python -c "import asyncpg; print('asyncpg installed')"
```

---

### **Issue 6: "Frontend won't start - Port 5173 in use"**

**Solution:**
```bash
# Find process using port 5173
# Windows:
netstat -ano | findstr :5173
taskkill /PID <process_id> /F

# Mac/Linux:
lsof -ti:5173 | xargs kill -9

# Or use different port:
npm run dev -- --port 3000
```

---

### **Issue 7: "CORS error in browser console"**

**Solution:**

Check `backend/app/main.py` CORS configuration:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

If using different port, add it to `allow_origins` list.

---

### **Issue 8: "Backend starts but API returns 404"**

**Check:**
1. Backend URL: http://127.0.0.1:8000
2. API docs: http://127.0.0.1:8000/docs
3. Health check: http://127.0.0.1:8000/health

If `/docs` works, API is running correctly!

---

### **Issue 9: "Virtual environment activation fails"**

**Windows PowerShell:**
```powershell
# Enable script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate
venv\Scripts\Activate.ps1
```

**Windows CMD:**
```cmd
venv\Scripts\activate.bat
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

---

### **Issue 10: "Dashboard shows no data"**

**Solution:**

1. **Check backend terminal** - Look for SQLAlchemy queries
2. **Check browser console** (F12) - Look for errors
3. **Verify database has data:**
   ```bash
   cd backend
   python -c "
   import asyncio
   from app.database import engine
   from sqlalchemy import text
   
   async def check():
       async with engine.connect() as conn:
           result = await conn.execute(text('SELECT COUNT(*) FROM requests'))
           print(f'Requests: {result.scalar()}')
   
   asyncio.run(check())
   "
   ```

---

## 📖 PROJECT INFORMATION

### **About This System**

The **Apartment Maintenance Request System** is a comprehensive full-stack application for managing maintenance operations in multi-unit residential buildings.

**Key Features:**
- 🏢 **Building Management** - Track multiple apartment buildings
- 🏠 **Unit Management** - Manage apartment units with occupancy status
- 👥 **Tenant Management** - Resident profiles with lease information
- 👷 **Staff Management** - Maintenance personnel with specialties
- 🔧 **Request Management** - Complete maintenance request lifecycle
- 📊 **Analytics Dashboard** - Real-time metrics and visualizations
- ⚡ **SLA Tracking** - Monitor response times and breaches
- 📝 **Assignment History** - Track work assignments with timestamps
- 💬 **Notes System** - Communication thread for each request

---

### **Technology Stack**

**Backend:**
- **Framework:** FastAPI 0.104.1 (Python 3.12)
- **Database:** PostgreSQL (NEON Cloud - Serverless)
- **ORM:** SQLAlchemy 2.0.23 (Async)
- **Database Driver:** AsyncPG 0.29.0
- **Validation:** Pydantic 2.5.0
- **ASGI Server:** Uvicorn 0.24.0

**Frontend:**
- **Framework:** React 18.2.0
- **Build Tool:** Vite 5.0.8
- **Routing:** React Router DOM 6.20.0
- **HTTP Client:** Axios 1.6.2
- **Charts:** Recharts 2.10.3
- **Styling:** TailwindCSS 3.3.6
- **Icons:** Lucide React 0.294.0

**Database Schema:**
- 5 main entities (Building, Unit, Tenant, Staff, Request)
- 3 ENUM types (IssueType, Priority, RequestStatus)
- Foreign key relationships with CASCADE/SET NULL
- JSON columns for complex data (assignments, notes, emergency contacts)

---

### **Database Structure**

```
BUILDING (1) ──────< (M) UNIT (1) ──────< (M) TENANT (1) ──────< (M) REQUEST
    │                    │                                              │
    └────────────────────┴──────────────────────────────────────────────┘
                                                                         │
                                                            STAFF ───────┘
                                                         (referenced in JSON)
```

**Tables:**
- **buildings** - 5 records (Boston neighborhoods)
- **units** - 200 records (40 per building)
- **tenants** - 100 records (50% occupancy)
- **staff** - 5 records (various specialties)
- **requests** - 200 records (various statuses)

---

### **API Endpoints**

**Base URL:** http://127.0.0.1:8000

**Buildings:**
- `GET /buildings` - List all buildings
- `POST /buildings` - Create building
- `GET /buildings/{id}` - Get building details
- `PUT /buildings/{id}` - Update building
- `DELETE /buildings/{id}` - Delete building

**Units:**
- `GET /units` - List all units
- `POST /units` - Create unit
- `GET /units/{id}` - Get unit details
- `PUT /units/{id}` - Update unit
- `DELETE /units/{id}` - Delete unit

**Tenants:**
- `GET /tenants` - List all tenants
- `POST /tenants` - Create tenant
- `GET /tenants/{id}` - Get tenant details
- `PUT /tenants/{id}` - Update tenant
- `DELETE /tenants/{id}` - Delete tenant

**Staff:**
- `GET /staff` - List all staff
- `POST /staff` - Create staff
- `GET /staff/{id}` - Get staff details
- `PUT /staff/{id}` - Update staff
- `DELETE /staff/{id}` - Soft delete staff

**Requests:**
- `GET /requests` - List all requests (with filters)
- `POST /requests` - Create request
- `GET /requests/{id}` - Get request details
- `PUT /requests/{id}` - Update request
- `PATCH /requests/{id}/status` - Update status
- `POST /requests/{id}/assign` - Assign to staff
- `POST /requests/{id}/notes` - Add note
- `DELETE /requests/{id}` - Delete request

**Metrics:**
- `GET /metrics/overview` - Dashboard KPIs
- `GET /metrics/requests-by-status` - Status distribution
- `GET /metrics/requests-by-priority` - Priority distribution
- `GET /metrics/requests-over-time` - Time series data
- `GET /metrics/building-performance` - Building metrics
- `GET /metrics/staff-performance` - Staff metrics

**Full API Documentation:** http://127.0.0.1:8000/docs (Swagger UI)

---

### **Environment Variables**

Located in `backend/.env`:

```properties
# PostgreSQL Configuration
PG_HOST=ep-broad-resonance-ade3fcco-pooler.c-2.us-east-1.aws.neon.tech
PG_DATABASE=neondb
PG_USER=neondb_owner
PG_PASSWORD=npg_SkIJU01uZvKo
PG_SSLMODE=require
PG_PORT=5432

# Application
SECRET_KEY=apartment-maintenance-secret-key-2025-pa55
API_HOST=0.0.0.0
API_PORT=8000
FRONTEND_URL=http://localhost:5173
ENVIRONMENT=development
```

**⚠️ Security Note:** For production deployment, change `SECRET_KEY` and secure database credentials.

---

### **File Structure**

```
apartment-maintenance-system/
│
├── backend/                      # FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # Application entry point
│   │   ├── config.py            # Configuration settings
│   │   ├── database.py          # Database connection
│   │   ├── models/              # Data models
│   │   │   ├── db_models.py    # SQLAlchemy ORM models
│   │   │   └── schemas.py      # Pydantic schemas
│   │   └── routers/             # API endpoints
│   │       ├── buildings.py
│   │       ├── units.py
│   │       ├── tenants.py
│   │       ├── staff.py
│   │       ├── requests.py
│   │       └── metrics.py
│   ├── init_db.py               # Database initialization
│   ├── seed_pg_data.py          # Data seeding script
│   ├── requirements.txt         # Python dependencies
│   ├── .env                     # Environment variables
│   └── venv/                    # Virtual environment (created)
│
├── frontend/                     # React Frontend
│   ├── src/
│   │   ├── App.jsx              # Main app component
│   │   ├── main.jsx             # Entry point
│   │   ├── components/          # React components
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Buildings.jsx
│   │   │   ├── Units.jsx
│   │   │   ├── Tenants.jsx
│   │   │   ├── Staff.jsx
│   │   │   └── Requests.jsx
│   │   ├── services/
│   │   │   └── api.js          # Axios API client
│   │   └── index.css           # TailwindCSS styles
│   ├── public/                  # Static assets
│   ├── package.json             # Node.js dependencies
│   ├── vite.config.js          # Vite configuration
│   ├── tailwind.config.js      # TailwindCSS config
│   └── node_modules/           # Dependencies (created)
│
├── README.md                    # This file
├── SETUP_GUIDE.md              # Additional setup info
└── .gitignore                  # Git ignore rules
```

---

## 📚 ADDITIONAL DOCUMENTATION

**In Project Root:**
- `FINAL_SUBMISSION_GUIDE.md` - Academic documentation
- `SCREENSHOT_CHECKLIST.md` - Screenshot guide for demos
- `ER_DIAGRAM_GUIDE.md` - Database diagram reference
- `WORD_DOCUMENT_TEMPLATE.md` - Complete project documentation

**API Documentation:**
- Swagger UI: http://127.0.0.1:8000/docs (when backend running)
- ReDoc: http://127.0.0.1:8000/redoc (alternative format)

---

## 🚀 DEPLOYMENT TO PRODUCTION

### **For Cloud Hosting:**

**Backend Options:**
- **Railway:** https://railway.app (easiest)
- **Render:** https://render.com (free tier)
- **Heroku:** https://heroku.com
- **AWS EC2:** https://aws.amazon.com/ec2/
- **DigitalOcean:** https://www.digitalocean.com/

**Frontend Options:**
- **Vercel:** https://vercel.com (recommended for Vite)
- **Netlify:** https://netlify.com
- **GitHub Pages:** https://pages.github.com
- **Cloudflare Pages:** https://pages.cloudflare.com

**Database:**
- Already using NEON PostgreSQL (cloud) ✅
- No additional database setup needed
- Connection pooling included

**Deployment Steps:**
1. Build frontend: `npm run build`
2. Deploy backend to cloud service
3. Deploy frontend dist/ to CDN
4. Update CORS origins in backend
5. Update API URL in frontend

---

## 📞 SUPPORT & CONTACT

**For Technical Issues:**
1. Check troubleshooting section above
2. Review backend terminal for error messages
3. Check browser console (F12) for frontend errors
4. Verify database connection in NEON console

**Database Access:**
- Console: https://console.neon.tech
- You have been added as a collaborator
- Can view and query database

**Resources:**
- FastAPI Docs: https://fastapi.tiangolo.com
- React Docs: https://react.dev
- SQLAlchemy Docs: https://docs.sqlalchemy.org
- NEON Docs: https://neon.tech/docs

---

## ✅ PRE-DEMO CHECKLIST

**Before presenting to professor:**

- [ ] Python 3.12+ installed
- [ ] Node.js 18+ installed
- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] Frontend dependencies installed (`npm install`)
- [ ] Both servers start without errors
- [ ] Dashboard loads at http://localhost:5173
- [ ] Data is visible (buildings, requests, etc.)
- [ ] Charts are displaying
- [ ] Can create new request
- [ ] Can view request details
- [ ] Internet connection active (for database)
- [ ] Browser is Chrome/Edge/Firefox (latest version)
- [ ] Screen resolution set to 1920x1080 or higher
- [ ] Zoom level at 100% in browser

**Test Run (2 minutes before demo):**
1. Start backend
2. Wait for "Connected to PostgreSQL: neondb"
3. Start frontend
4. Open http://localhost:5173
5. Verify dashboard loads
6. Navigate to Requests section
7. Click on a request to view details

**✅ You're ready to present!**

---

## 📄 LICENSE & CREDITS

**Project:** Apartment Maintenance Request System  
**Course:** FA25 – Applied Database Technologies (12751)  
**Team:** Nerice Rodrigues & Rachana H Dharani  
**Date:** November 2025  
**Database:** NEON PostgreSQL (Serverless)

**Technologies Used:**
- FastAPI (MIT License)
- React (MIT License)
- SQLAlchemy (MIT License)
- TailwindCSS (MIT License)
- Vite (MIT License)
- And 30+ open source libraries

---

## 🎉 GOOD LUCK WITH YOUR DEMO!

**The system is production-ready and fully functional!**

If you encounter any issues during setup, follow the troubleshooting section or verify:
1. Backend terminal shows "Connected to PostgreSQL: neondb"
2. Frontend terminal shows "ready in XXXms"
3. Browser shows dashboard with data

**You've got this! 💪✨**
