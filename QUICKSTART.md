# Quick Start Guide
## Apartment Maintenance Request System

This guide will help you get the application running in **under 15 minutes**.

---

## 📋 Prerequisites Checklist

Before starting, ensure you have:
- [ ] Python 3.10+ installed
- [ ] Node.js 18+ installed
- [ ] MongoDB Atlas account (free) OR local MongoDB
- [ ] Git installed
- [ ] PowerShell or Terminal access

---

## 🚀 5-Minute Setup

### Step 1: Clone and Navigate (30 seconds)

```powershell
cd "c:\Users\prInce dabre\Downloads\18s projects\nerice noob\MongoDB\apartment-maintenance-system"
```

### Step 2: Setup MongoDB Atlas (3 minutes)

**Option A: MongoDB Atlas (Recommended)**

1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up for free account
3. Create a new cluster (M0 Free tier)
4. Create database user: `admin` / `YourPassword123`
5. Add IP: `0.0.0.0/0` (for development)
6. Click "Connect" → "Connect your application"
7. Copy connection string (looks like):
   ```
   mongodb+srv://admin:YourPassword123@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```

**Option B: Local MongoDB**
```powershell
# Using Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

### Step 3: Backend Setup (2 minutes)

```powershell
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate (PowerShell)
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create .env file
Copy-Item ..\.env.example -Destination .env

# Edit .env file with your MongoDB URI
notepad .env
```

**Edit .env file:**
```env
MONGO_URI=mongodb+srv://admin:YourPassword123@cluster0.xxxxx.mongodb.net/apartment_maintenance?retryWrites=true&w=majority
MONGO_DB_NAME=apartment_maintenance
SECRET_KEY=your-secret-key-change-this-in-production
API_HOST=0.0.0.0
API_PORT=8000
FRONTEND_URL=http://localhost:5173
ENVIRONMENT=development
```

### Step 4: Seed Database (1 minute)

```powershell
# From backend directory, activate venv if not already
.\venv\Scripts\Activate.ps1

# Navigate to scripts
cd ..\scripts

# Run seeding script
python seed_data.py --mongo "YOUR_MONGO_URI_HERE"

# This creates:
# - 5 buildings
# - 200 units
# - 100 tenants
# - 5 staff members
# - 200 maintenance requests
```

### Step 5: Start Backend (30 seconds)

```powershell
# Navigate back to backend
cd ..\backend

# Activate venv
.\venv\Scripts\Activate.ps1

# Start server
uvicorn app.main:app --reload
```

✅ Backend running at http://localhost:8000  
📚 API Docs at http://localhost:8000/docs

### Step 6: Frontend Setup (2 minutes)

**Open a NEW PowerShell window:**

```powershell
# Navigate to frontend
cd "c:\Users\prInce dabre\Downloads\18s projects\nerice noob\MongoDB\apartment-maintenance-system\frontend"

# Install dependencies
npm install

# Create .env file
Copy-Item .env.example -Destination .env

# Start development server
npm run dev
```

✅ Frontend running at http://localhost:5173

---

## ✅ Verification

Open browser to http://localhost:5173

You should see:
- Dashboard with metrics and charts
- Navigation menu (Dashboard, Requests, Tenants, Staff)
- Sample data populated from seeding script

Test the API:
- http://localhost:8000/docs - Interactive API documentation
- http://localhost:8000/metrics/overview - Get metrics JSON

---

## 🎯 Common Commands

### Backend Commands
```powershell
cd backend
.\venv\Scripts\Activate.ps1

# Run server
uvicorn app.main:app --reload

# Run tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=html
```

### Frontend Commands
```powershell
cd frontend

# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run tests
npm test
```

### Database Commands
```powershell
cd scripts

# Seed database
python seed_data.py --mongo "YOUR_MONGO_URI"

# Clear and reseed
python seed_data.py --mongo "YOUR_MONGO_URI" --clear
```

---

## 🐛 Troubleshooting

### Backend won't start
```powershell
# Check if port 8000 is in use
netstat -ano | findstr :8000

# If in use, kill process or use different port
uvicorn app.main:app --reload --port 8001
```

### MongoDB connection fails
- Verify connection string in `.env`
- Check network access in MongoDB Atlas (IP whitelist)
- Ensure username/password are correct (URL encoded if special chars)

### Frontend build errors
```powershell
# Clear node_modules and reinstall
Remove-Item -Recurse -Force node_modules
npm install

# Clear Vite cache
Remove-Item -Recurse -Force node_modules/.vite
```

### Can't install Python packages
```powershell
# Upgrade pip
python -m pip install --upgrade pip

# Try with --user flag
pip install --user -r requirements.txt
```

---

## 📦 Project Structure

```
apartment-maintenance-system/
├── backend/               # FastAPI backend
│   ├── app/
│   │   ├── routers/      # API endpoints
│   │   ├── models/       # Pydantic schemas
│   │   └── main.py       # FastAPI app
│   └── requirements.txt
├── frontend/              # React frontend
│   ├── src/
│   │   ├── pages/        # Page components
│   │   ├── components/   # Reusable components
│   │   └── services/     # API services
│   └── package.json
├── scripts/
│   └── seed_data.py      # Database seeding
└── README.md
```

---

## 📚 Next Steps

1. **Explore the API**: http://localhost:8000/docs
2. **Browse Dashboard**: View analytics and metrics
3. **Create Requests**: Test the create request form
4. **Customize**: Modify colors in `tailwind.config.js`
5. **Add Features**: Extend with additional endpoints or pages

---

## 🎓 Learning Resources

- **FastAPI**: https://fastapi.tiangolo.com/
- **MongoDB**: https://docs.mongodb.com/
- **React**: https://react.dev/
- **Recharts**: https://recharts.org/
- **TailwindCSS**: https://tailwindcss.com/

---

## 🤝 Support

If you encounter issues:
1. Check error messages in terminal
2. Review backend logs
3. Check browser console (F12)
4. Verify all environment variables are set
5. Ensure MongoDB is accessible

---

**Ready to Deploy?** See [README.md](README.md) for deployment instructions to Render and Vercel.

**Need Help?** Contact: nerodr@iu.edu, rdharani@iu.edu

---

**Last Updated**: November 7, 2025  
**Project**: PA55 Final Project Milestone 2
