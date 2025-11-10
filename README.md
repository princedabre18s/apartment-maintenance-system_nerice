# Apartment Maintenance Request System# Apartment Maintenance Request System# Apartment Maintenance Request System



## 🚀 Quick Installation & Setup



### Prerequisites## 🚀 Quick Installation & SetupA full-stack web application for managing apartment maintenance requests using MongoDB, FastAPI, and React.

- **Python 3.12+** ([Download](https://www.python.org/downloads/))

- **Node.js 18+** ([Download](https://nodejs.org/))



### Installation Steps### Prerequisites## 🎯 Project Overview



#### 1. Backend Setup (5 minutes)- **Python 3.12+** ([Download](https://www.python.org/downloads/))



```bash- **Node.js 18+** ([Download](https://nodejs.org/))This system allows tenants to submit and track maintenance issues while enabling staff and administrators to efficiently manage, assign, and monitor these requests. The application features comprehensive CRUD operations, real-time analytics, and data visualizations.

# Navigate to backend directory

cd apartment-maintenance-system/backend- **Git** (optional)



# Create virtual environment**Academic Project**: PA55: APPLIED DATABASE TECHNOLOGIES (Fall 2025)  

python -m venv venv

### Installation Steps**Team Members**: Nerodr & Rdharani  

# Activate virtual environment

# On Windows:**Milestone**: Final Project Milestone 2

venv\Scripts\activate

# On Mac/Linux:#### 1. Backend Setup (5 minutes)

source venv/bin/activate

## 📋 Table of Contents

# Install all dependencies

pip install -r requirements.txt```bash

```

# Navigate to backend directory- [Features](#features)

#### 2. Frontend Setup (3 minutes)

cd apartment-maintenance-system/backend- [Tech Stack](#tech-stack)

```bash

# Navigate to frontend directory (open new terminal)- [Prerequisites](#prerequisites)

cd apartment-maintenance-system/frontend

# Create virtual environment- [Installation & Setup](#installation--setup)

# Install dependencies

npm installpython -m venv venv- [Database Schema](#database-schema)

```

- [API Documentation](#api-documentation)

### ▶️ Running the Application

# Activate virtual environment- [Running the Application](#running-the-application)

#### Method 1: Two Terminals (Recommended for Demo)

# On Windows:- [Testing](#testing)

**Terminal 1 - Backend:**

```bashvenv\Scripts\activate- [Data Seeding](#data-seeding)

cd backend

venv\Scripts\activate# On Mac/Linux:- [Deployment](#deployment)

uvicorn app.main:app --reload

```source venv/bin/activate- [Contributing](#contributing)

✅ Backend running at: http://127.0.0.1:8000

- [AI Tool Acknowledgment](#ai-tool-acknowledgment)

**Terminal 2 - Frontend:**

```bash# Install all dependencies

cd frontend

npm run devpip install -r requirements.txt## ✨ Features

```

✅ Frontend running at: http://localhost:5173```



#### Method 2: Windows Batch Script (Easiest!)### Core Functionality



Double-click `start-demo.bat` file in the root directory.#### 2. Frontend Setup (3 minutes)- **Tenant Management**: Create, read, update, and delete tenant profiles

- Opens 2 command windows automatically

- Starts both backend and frontend- **Building & Unit Management**: Manage buildings and their associated units

- Opens browser to http://localhost:5173

```bash- **Maintenance Requests**: Full CRUD operations for maintenance issues

### 🎯 For Professor Demo

# Navigate to frontend directory (open new terminal)- **Staff Assignments**: Assign staff to requests and track completion

1. **Start Application**: Use Method 1 or 2 above

2. **Wait 10 seconds** for both servers to initializecd apartment-maintenance-system/frontend- **Communication**: Add notes and updates to requests

3. **Open Browser**: Go to http://localhost:5173

4. **Dashboard Opens Automatically** - No login required!- **Real-time Status Tracking**: Monitor request statuses from open to closed



5. **Database Status**: ✅ Already populated with 510 records# Install dependencies

   - 5 Buildings

   - 200 Apartment Unitsnpm install### Analytics & Visualizations

   - 100 Tenants

   - 5 Staff Members```- **Dashboard Metrics**:

   - 200 Maintenance Requests

  - Total open vs. closed requests

### 🔧 Troubleshooting

### ▶️ Running the Application  - Average resolution time

**Port Already in Use:**

```bash  - Top 5 issue categories

# Backend (port 8000)

netstat -ano | findstr :8000#### Method 1: Two Terminals (Recommended for Demo)  - SLA breach monitoring

taskkill /PID <PID> /F

  - Completion rates

# Frontend (port 5173)

netstat -ano | findstr :5173**Terminal 1 - Backend:**- **Interactive Charts** (using Recharts):

taskkill /PID <PID> /F

``````bash  - Bar charts for issue types



**Module Not Found Error:**cd backend  - Pie charts for status distribution

```bash

cd backendvenv\Scripts\activate  - Line charts for request trends over time

venv\Scripts\activate

pip install -r requirements.txt --force-reinstalluvicorn app.main:app --reload  - KPI cards for key metrics

```

```

**Database Connection Error:**

- Check `backend/.env` file exists✅ Backend running at: http://127.0.0.1:8000## 🛠️ Tech Stack

- Verify NEON database credentials are correct

- Ensure internet connection is active



**npm Install Fails:****Terminal 2 - Frontend:**### Backend

```bash

cd frontend```bash- **Framework**: FastAPI (Python)

npm cache clean --force

npm installcd frontend- **Database**: MongoDB with Motor (async driver)

```

npm run dev- **Data Validation**: Pydantic v2

---

```- **API Documentation**: Auto-generated OpenAPI (Swagger)

## 📋 Project Information

✅ Frontend running at: http://localhost:5173

**Academic Project**: PA55: APPLIED DATABASE TECHNOLOGIES (Fall 2025)  

**Team Members**: Nerodr & Rdharani  ### Frontend

**Milestone**: Final Project Milestone 2

#### Method 2: Windows Batch Script (Easiest!)- **Framework**: React 18 + Vite

### About the System

- **Styling**: TailwindCSS

**Apartment Maintenance Request System** is a comprehensive web application designed to streamline the maintenance request process in residential apartment complexes. It provides a centralized platform for tenants to submit maintenance requests, staff to manage and track work orders, and administrators to oversee operations.

Double-click `start-demo.bat` file in the root directory.- **Routing**: React Router v6

### Key Features

- Opens 2 command windows automatically- **Charts**: Recharts

✅ **Full CRUD Operations**

- Buildings, Units, Tenants, Staff, and Maintenance Requests- Starts both backend and frontend- **HTTP Client**: Axios

- Real-time data updates

- Form validation and error handling- Opens browser to http://localhost:5173



✅ **Dashboard & Analytics**### Testing

- Interactive charts and visualizations

- Request status tracking### 🎯 For Professor Demo- **Backend**: Pytest + pytest-asyncio

- Staff performance metrics

- Building-wise statistics- **Frontend**: Jest + React Testing Library



✅ **Request Management**1. **Start Application**: Use Method 1 or 2 above

- Create, view, update, and delete requests

- Assign staff to requests2. **Wait 10 seconds** for both servers to initialize### Deployment

- Add notes and updates

- Track request history3. **Open Browser**: Go to http://localhost:5173- **Backend**: Render / Railway



### Technology Stack4. **Login Credentials**:- **Frontend**: Vercel / Netlify



**Backend:**   - **Admin**: admin@example.com / password: admin123- **Database**: MongoDB Atlas

- FastAPI 0.104.1 (Python web framework)

- SQLAlchemy 2.0.23 (ORM)   - **Tenant**: tenant@example.com / password: tenant123

- AsyncPG 0.30.0 (PostgreSQL async driver)

- Pydantic 2.5.0 (Data validation)   - **Staff**: staff@example.com / password: staff123## 📦 Prerequisites

- Uvicorn 0.24.0 (ASGI server)



**Frontend:**

- React 18.2.05. **Database Status**: ✅ Already populated with 510 records- **Python**: 3.10 or higher

- Vite 5.0.8 (Build tool)

- React Router DOM 6.20.0   - 5 Buildings- **Node.js**: 18 or higher

- Axios 1.6.2 (HTTP client)

- TailwindCSS 3.3.6 (Styling)   - 200 Apartment Units- **MongoDB**: Atlas account or local instance

- Recharts 2.10.3 (Charts)

   - 100 Tenants- **Git**: For version control

**Database:**

- PostgreSQL (NEON Serverless)   - 5 Staff Members

- Cloud-hosted with SSL encryption

- Connection pooling enabled   - 200 Maintenance Requests## 🚀 Installation & Setup



### Database Structure



**Core Tables:**### 🔧 Troubleshooting### 1. Clone the Repository

- `buildings` - Apartment complex information

- `units` - Individual apartment units

- `tenants` - Resident information

- `staff` - Maintenance staff details**Port Already in Use:**```powershell

- `maintenance_requests` - Work order tracking

- `request_assignments` - Staff-to-request mapping```bashgit clone https://github.com/yourusername/apartment-maintenance-system.git



### API Endpoints# Backend (port 8000)cd apartment-maintenance-system



**Base URL:** http://127.0.0.1:8000netstat -ano | findstr :8000```



**Buildings:** GET, POST, PUT, DELETE `/api/buildings`  taskkill /PID <PID> /F

**Units:** GET, POST, PUT, DELETE `/api/units`  

**Tenants:** GET, POST, PUT, DELETE `/api/tenants`  ### 2. Backend Setup

**Staff:** GET, POST, PUT, DELETE `/api/staff`  

**Maintenance Requests:** GET, POST, PUT, DELETE `/api/maintenance-requests`  # Frontend (port 5173)

**Analytics:** GET `/api/analytics/dashboard`

netstat -ano | findstr :5173```powershell

---

taskkill /PID <PID> /F# Navigate to backend directory

## 🎓 Demo Checklist

```cd backend

Before presenting to professor:



- [ ] Both servers running (check Terminal 1 & 2)

- [ ] Browser open to http://localhost:5173**Module Not Found Error:**# Create virtual environment

- [ ] Dashboard loads with charts

- [ ] Internet connection active (for database)```bashpython -m venv venv

- [ ] Demo data loaded (510 records)

- [ ] No console errors visiblecd backend



**Tip:** Run the application once before the demo to ensure everything works smoothly!venv\Scripts\activate# Activate virtual environment (Windows PowerShell)



---pip install -r requirements.txt --force-reinstall.\venv\Scripts\Activate.ps1



## 📦 For Domain Deployment```



This project is ready for production deployment. Key steps:# Install dependencies



1. **Backend Hosting**: Deploy to AWS, Azure, Heroku, or DigitalOcean**Database Connection Error:**pip install -r requirements.txt

2. **Frontend Hosting**: Deploy to Vercel, Netlify, or same server as backend

3. **Database**: Already using NEON (cloud PostgreSQL) - production ready- Check `backend/.env` file exists

4. **Environment Variables**: Update `FRONTEND_URL` and `API_HOST` in `.env`

- Verify NEON database credentials are correct# Create .env file (copy from .env.example)

See `DEPLOYMENT_README.md` for detailed production deployment guide.

- Ensure internet connection is activeCopy-Item ..\.env.example -Destination .env

---



## 🤖 AI Tool Acknowledgment

**npm Install Fails:**# Edit .env file with your MongoDB connection string

**Important**: This project utilized AI coding assistants during development.

```bash# MONGO_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<database>

### Tools Used

- **GitHub Copilot** (GPT-4 model)cd frontend```

- **Accessed**: November 2025

- **IDE**: Visual Studio Codenpm cache clean --force



### Scope of Usenpm install### 3. Frontend Setup

AI tools assisted with:

- Code generation (boilerplate, API routes, React components)```

- Refactoring and code structure improvements

- Documentation and comments```powershell

- Debugging and error fixes

- Data generation logic---# Navigate to frontend directory (from project root)



All AI-generated code was reviewed, tested, and modified by the team.cd frontend



---## 📋 Project Information



**Version:** 1.0.0  # Install dependencies

**Last Updated:** November 2025  

**License:** MIT**Academic Project**: PA55: APPLIED DATABASE TECHNOLOGIES (Fall 2025)  npm install


**Team Members**: Nerodr & Rdharani  

**Milestone**: Final Project Milestone 2# Create .env file

Copy-Item .env.example -Destination .env

### About the System

# Edit .env file with backend URL

**Apartment Maintenance Request System** is a comprehensive web application designed to streamline the maintenance request process in residential apartment complexes. It provides a centralized platform for tenants to submit maintenance requests, staff to manage and track work orders, and administrators to oversee operations.# VITE_API_URL=http://localhost:8000

```

### Key Features

### 4. MongoDB Setup

✅ **Tenant Portal**

- Submit maintenance requests with photos#### Option A: MongoDB Atlas (Cloud)

- Track request status in real-time1. Create a free account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)

- View request history2. Create a new cluster

- Receive notifications3. Set up database access (username/password)

4. Whitelist your IP address (or use 0.0.0.0/0 for development)

✅ **Staff Management**5. Get your connection string and update `.env` file

- View assigned maintenance tasks

- Update request status and progress#### Option B: Local MongoDB

- Add work notes and completion details```powershell

- Manage work schedules# Install MongoDB locally or use Docker

docker run -d -p 27017:27017 --name mongodb mongo:latest

✅ **Admin Dashboard**

- Comprehensive analytics and reports# Update .env with local connection

- Manage buildings, units, and tenants# MONGO_URI=mongodb://localhost:27017/apartment_maintenance

- Staff assignment and tracking```

- Request prioritization and routing

## 🗄️ Database Schema

### Technology Stack

The system uses 5 main collections:

**Backend:**

- FastAPI 0.104.1 (Python web framework)### Collections

- SQLAlchemy 2.0.23 (ORM)

- AsyncPG 0.30.0 (PostgreSQL async driver)1. **buildings**: Apartment building information

- Pydantic 2.5.0 (Data validation)2. **units**: Individual apartment units

- Uvicorn 0.24.0 (ASGI server)3. **tenants**: Tenant profiles and lease information

4. **staff**: Maintenance staff and administrators

**Frontend:**5. **requests**: Maintenance requests with embedded assignments and notes

- React 18.2.0

- Vite 5.0.8 (Build tool)For detailed schema documentation, see [SCHEMA.md](SCHEMA.md).

- React Router DOM 6.20.0

- Axios 1.6.2 (HTTP client)### Entity Relationships

- TailwindCSS 3.3.6 (Styling)

- Recharts 2.10.3 (Charts)```

buildings (1) ──→ (M) units

**Database:**units (1) ──→ (M) tenants

- PostgreSQL (NEON Serverless)tenants (1) ──→ (M) requests

- Cloud-hosted with SSL encryptionstaff (1) ──→ (M) assignments (embedded in requests)

- Connection pooling enabled```



### Database Structure## 📡 API Documentation



**Core Tables:**### Base URL

- `buildings` - Apartment complex information```

- `units` - Individual apartment unitshttp://localhost:8000

- `tenants` - Resident information```

- `staff` - Maintenance staff details

- `maintenance_requests` - Work order tracking### API Endpoints

- `request_assignments` - Staff-to-request mapping

#### Buildings

### API Endpoints- `GET /buildings/` - Get all buildings

- `GET /buildings/{id}` - Get specific building

**Base URL:** http://127.0.0.1:8000- `POST /buildings/` - Create building

- `PUT /buildings/{id}` - Update building

**Buildings:**- `DELETE /buildings/{id}` - Delete building

- `GET /api/buildings` - List all buildings

- `POST /api/buildings` - Create building#### Units

- `GET /api/buildings/{id}` - Get building details- `GET /units/` - Get all units

- `PUT /api/buildings/{id}` - Update building- `GET /units/{id}` - Get specific unit

- `DELETE /api/buildings/{id}` - Delete building- `POST /units/` - Create unit

- `PUT /units/{id}` - Update unit

**Units:**- `DELETE /units/{id}` - Delete unit

- `GET /api/units` - List all units

- `POST /api/units` - Create unit#### Tenants

- `GET /api/units/{id}` - Get unit details- `GET /tenants/` - Get all tenants

- `PUT /api/units/{id}` - Update unit- `GET /tenants/{id}` - Get specific tenant

- `POST /tenants/` - Create tenant

**Tenants:**- `PUT /tenants/{id}` - Update tenant

- `GET /api/tenants` - List all tenants- `DELETE /tenants/{id}` - Delete tenant

- `POST /api/tenants` - Create tenant

- `GET /api/tenants/{id}` - Get tenant details#### Staff

- `PUT /api/tenants/{id}` - Update tenant- `GET /staff/` - Get all staff

- `GET /staff/{id}` - Get specific staff member

**Maintenance Requests:**- `POST /staff/` - Create staff member

- `GET /api/maintenance-requests` - List requests- `PUT /staff/{id}` - Update staff member

- `POST /api/maintenance-requests` - Create request- `DELETE /staff/{id}` - Deactivate staff member

- `GET /api/maintenance-requests/{id}` - Get request details

- `PUT /api/maintenance-requests/{id}` - Update request#### Requests

- `DELETE /api/maintenance-requests/{id}` - Delete request- `GET /requests/` - Get all requests (with filters)

- `GET /requests/{id}` - Get specific request

**Staff:**- `POST /requests/` - Create request

- `GET /api/staff` - List all staff- `PUT /requests/{id}` - Update request

- `POST /api/staff` - Create staff member- `DELETE /requests/{id}` - Delete request

- `GET /api/staff/{id}` - Get staff details- `POST /requests/{id}/assign` - Assign staff to request

- `PUT /api/staff/{id}` - Update staff- `POST /requests/{id}/notes` - Add note to request

- `POST /requests/{id}/complete` - Mark assignment complete

**Analytics:**

- `GET /api/analytics/dashboard` - Dashboard statistics#### Metrics

- `GET /api/analytics/requests-by-status` - Status breakdown- `GET /metrics/overview` - Dashboard overview

- `GET /api/analytics/requests-by-priority` - Priority distribution- `GET /metrics/requests-by-status` - Requests grouped by status

- `GET /metrics/requests-by-priority` - Requests grouped by priority

### File Structure- `GET /metrics/requests-over-time` - Time series data

- `GET /metrics/building-performance` - Performance by building

```- `GET /metrics/staff-performance` - Performance by staff member

apartment-maintenance-system/

├── backend/### Interactive API Documentation

│   ├── app/

│   │   ├── main.py              # FastAPI application entryOnce the backend is running, visit:

│   │   ├── database.py          # Database connection- **Swagger UI**: http://localhost:8000/docs

│   │   ├── models.py            # SQLAlchemy models- **ReDoc**: http://localhost:8000/redoc

│   │   ├── schemas.py           # Pydantic schemas

│   │   ├── crud.py              # Database operations## 🏃 Running the Application

│   │   └── routers/             # API route handlers

│   ├── tests/                   # Unit tests### Start Backend Server

│   ├── .env                     # Environment variables (NEON credentials)

│   ├── requirements.txt         # Python dependencies```powershell

│   └── venv/                    # Virtual environment (created on install)cd backend

│

├── frontend/# Activate virtual environment

│   ├── src/.\venv\Scripts\Activate.ps1

│   │   ├── components/          # React components

│   │   ├── pages/               # Page components# Run with uvicorn

│   │   ├── services/            # API service layeruvicorn app.main:app --reload --host 0.0.0.0 --port 8000

│   │   ├── App.jsx              # Main application component```

│   │   └── main.jsx             # Entry point

│   ├── public/                  # Static assetsThe API will be available at `http://localhost:8000`

│   ├── package.json             # npm dependencies

│   ├── vite.config.js           # Vite configuration### Start Frontend Development Server

│   ├── tailwind.config.js       # TailwindCSS settings

│   └── node_modules/            # npm packages (created on install)```powershell

│cd frontend

├── README.md                    # This file (quick setup guide)

├── DEPLOYMENT_README.md         # Detailed deployment guide# Run development server

└── start-demo.bat               # Windows quick start scriptnpm run dev

``````



### Environment VariablesThe frontend will be available at `http://localhost:5173`



**Backend** (`backend/.env`):## 🧪 Testing

```env

# PostgreSQL (NEON Database) - Already Configured### Backend Tests

PG_HOST=ep-broad-resonance-ade3fcco-pooler.c-2.us-east-1.aws.neon.tech

PG_DATABASE=neondb```powershell

PG_USER=neondb_ownercd backend

PG_PASSWORD=npg_SkIJU01uZvKo

PG_SSLMODE=require# Activate virtual environment

PG_PORT=5432.\venv\Scripts\Activate.ps1



# API Configuration# Run tests

SECRET_KEY=your-secret-key-here-change-in-productionpytest

API_HOST=0.0.0.0

API_PORT=8000# Run with coverage

FRONTEND_URL=http://localhost:5173pytest --cov=app --cov-report=html

ENVIRONMENT=development

```# View coverage report

# Open htmlcov/index.html in browser

**Note:** Database credentials are already configured for collaborator access. No changes needed!```



### Support & Documentation### Frontend Tests



- **API Documentation**: http://127.0.0.1:8000/docs (when backend running)```powershell

- **Detailed Deployment Guide**: See `DEPLOYMENT_README.md`cd frontend

- **Testing**: Run `pytest` in backend directory (with venv activated)

# Run tests

### Development Teamnpm test



Developed for apartment complex maintenance management with focus on user experience and operational efficiency.# Run with coverage

npm test -- --coverage

---```



## 🎓 Demo Checklist## 📊 Data Seeding



Before presenting to professor:Populate the database with sample data:



- [ ] Both servers running (check Terminal 1 & 2)```powershell

- [ ] Browser open to http://localhost:5173cd scripts

- [ ] Login credentials ready (see above)

- [ ] Internet connection active (for database)# Basic seeding (generates sample data)

- [ ] Demo data loaded (510 records)python seed_data.py --mongo "your_mongodb_uri"

- [ ] No console errors visible

# With Boston 311 CSV data (if available)

**Tip:** Run the application once before the demo to ensure everything works smoothly!python seed_data.py --mongo "your_mongodb_uri" --csv "../data/boston_311_sample.csv"

```

---

This will create:

## 📦 For Domain Deployment- 5 buildings

- 200 units (40 per building)

This project is ready for production deployment. Key steps:- 100 tenants

- 5 staff members

1. **Backend Hosting**: Deploy to AWS, Azure, Heroku, or DigitalOcean- 200 maintenance requests

2. **Frontend Hosting**: Deploy to Vercel, Netlify, or same server as backend- Proper indexes for optimal query performance

3. **Database**: Already using NEON (cloud PostgreSQL) - production ready

4. **Environment Variables**: Update `FRONTEND_URL` and `API_HOST` in `.env`## 🌐 Deployment

5. **Build Frontend**: Run `npm run build` in frontend directory

6. **Serve Static**: Use Nginx or serve frontend build with backend### Backend Deployment (Render)



See `DEPLOYMENT_README.md` for detailed production deployment guide.1. Create account at [Render.com](https://render.com)

2. Create new **Web Service**

---3. Connect your GitHub repository

4. Configure:

## 🤖 AI Tool Acknowledgment   - **Build Command**: `pip install -r backend/requirements.txt`

   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Important**: This project utilized AI coding assistants during development.   - **Environment Variables**: Add `MONGO_URI`, `SECRET_KEY`, etc.



### Tools Used### Frontend Deployment (Vercel)

- **GitHub Copilot** (GPT-4 model)

- **Version**: Accessed on November 7, 20251. Create account at [Vercel.com](https://vercel.com)

- **Visual Studio Code**: IntelliCode extension2. Import your GitHub repository

3. Configure:

### Scope of Use   - **Framework Preset**: Vite

AI tools were used for:   - **Root Directory**: `frontend`

1. **Code Generation**: Generating boilerplate code for API routes and React components   - **Environment Variables**: Add `VITE_API_URL`

2. **Refactoring**: Improving code structure and readability

3. **Documentation**: Assisting with README and code comments### MongoDB Atlas Configuration

4. **Debugging**: Suggesting fixes for syntax and logic errors

5. **Data Seeding**: Creating realistic sample data generation logic1. Update network access to allow connections from deployment platforms

2. Use connection string in environment variables

---3. Enable authentication and use secure passwords



**Version:** 1.0.0  ## 📈 Project Structure

**Last Updated:** 2025  

**License:** MIT```

apartment-maintenance-system/
├── backend/
│   ├── app/
│   │   ├── routers/          # API route handlers
│   │   ├── models/           # Pydantic schemas
│   │   ├── config.py         # Configuration settings
│   │   ├── database.py       # MongoDB connection
│   │   └── main.py           # FastAPI application
│   ├── tests/                # Backend tests
│   ├── requirements.txt      # Python dependencies
│   └── pytest.ini            # Pytest configuration
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── pages/            # Page components
│   │   ├── services/         # API services
│   │   ├── App.jsx           # Main app component
│   │   └── main.jsx          # Entry point
│   ├── package.json          # Node dependencies
│   └── vite.config.js        # Vite configuration
├── scripts/
│   └── seed_data.py          # Data seeding script
├── data/                     # Sample data files
├── SCHEMA.md                 # Database schema documentation
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## 👥 Contributing

This is an academic project for PA55: APPLIED DATABASE TECHNOLOGIES.

### Team Contribution Summary

| Name | Tasks | Hours |
|------|-------|-------|
| Nerodr | Backend API development, MongoDB schema design, data seeding | 40 |
| Rdharani | Frontend development, UI/UX design, analytics dashboard | 40 |

## 🤖 AI Tool Acknowledgment

**Important**: This project utilized AI coding assistants during development.

### Tools Used
- **GitHub Copilot** (GPT-4 model)
- **Version**: Accessed on November 7, 2025
- **Visual Studio Code**: IntelliCode extension

### Scope of Use
AI tools were used for:
1. **Code Generation**: Generating boilerplate code for API routes and React components
2. **Refactoring**: Improving code structure and readability
3. **Documentation**: Assisting with README and code comments
4. **Debugging**: Suggesting fixes for syntax and logic errors
5. **Data Seeding**: Creating realistic sample data generation logic

### Citation Format
```
Portions of this code were generated or refactored using:
- GitHub Copilot (GPT-4), accessed November 7, 2025
- For function/template/refactoring suggestions
```

All AI-generated code was reviewed, tested, and modified by the development team to ensure correctness and alignment with project requirements.

## 📄 License

This project is created for educational purposes as part of Indiana University's PA55 course.

## 📞 Contact

For questions or issues, please contact:
- **Email**: nerodr@iu.edu, rdharani@iu.edu
- **Course**: PA55: APPLIED DATABASE TECHNOLOGIES
- **Semester**: Fall 2025

## 🙏 Acknowledgments

- Professor and teaching staff of PA55
- MongoDB documentation and community
- FastAPI and React communities
- Boston 311 Open Data portal for sample dataset inspiration

---

**Project Status**: ✅ Complete  
**Last Updated**: November 7, 2025  
**Version**: 1.0.0
