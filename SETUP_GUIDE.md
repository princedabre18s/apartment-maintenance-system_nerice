# SETUP GUIDE - Read This First!

## 📦 What's Inside This Package?

This ZIP contains a complete, ready-to-run Apartment Maintenance Request System for your professor demo.

**Database Status:** ✅ Fully configured and populated (510 records)  
**Setup Time:** ~8 minutes  
**Demo Ready:** Immediately after setup

---

## 🎯 Quick Start (For Impatient People!)

1. **Extract this ZIP** to any folder on your PC
2. **Double-click** `start-demo.bat`
3. **Wait 20 seconds** for servers to start
4. **Browser opens automatically** to http://localhost:5173
5. **Login** with: admin@example.com / admin123

**That's it!** 🎉

*(First time users: Read the full guide below)*

---

## 📋 First-Time Setup (One-Time Only)

### Step 1: Install Python (if not installed)

1. Go to: https://www.python.org/downloads/
2. Download **Python 3.12** or higher
3. **IMPORTANT**: Check ✅ "Add Python to PATH" during installation
4. Verify: Open Command Prompt and type `python --version`

### Step 2: Install Node.js (if not installed)

1. Go to: https://nodejs.org/
2. Download **LTS version** (18.x or higher)
3. Install with default settings
4. Verify: Open Command Prompt and type `node --version`

### Step 3: Run Backend Setup (One Time)

```bash
# Open Command Prompt in project folder
cd apartment-maintenance-system

# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Install packages (takes 2-3 minutes)
pip install -r requirements.txt
```

**Wait for installation to complete!** You'll see: "Successfully installed..."

### Step 4: Run Frontend Setup (One Time)

```bash
# Open NEW Command Prompt in project folder
cd apartment-maintenance-system

# Navigate to frontend
cd frontend

# Install packages (takes 3-4 minutes)
npm install
```

**Wait for installation!** You'll see: "added XXX packages"

---

## ▶️ Running the Demo (Every Time)

### Option A: Windows Batch Script (Recommended!)

1. **Double-click** `start-demo.bat` in the project root
2. Two terminal windows will open (DON'T CLOSE THEM!)
3. Wait 15-20 seconds
4. Browser opens automatically

### Option B: Manual Start (2 Terminals)

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload
```
✅ Wait for: "Application startup complete"

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```
✅ Wait for: "Local: http://localhost:5173"

### Option C: Production Build (Optional)

```bash
# Frontend production build
cd frontend
npm run build

# Serve with backend
cd ../backend
venv\Scripts\activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## 🎯 Application Access

**No Login Required!**
- Application opens directly to the Dashboard
- Full access to all features immediately
- Navigate using the sidebar menu

---

## 🗄️ Database Information

**Status:** ✅ Already Configured (No Setup Required!)

**Database Type:** NEON PostgreSQL (Cloud)  
**Location:** AWS US-East-1  
**Records:** 510 total
- 5 Buildings
- 200 Apartment Units
- 100 Tenants
- 5 Staff Members
- 200 Maintenance Requests

**Credentials:** Already in `backend/.env` file  
**Collaborator Access:** You have full access to the database  
**Connection:** Requires internet (cloud database)

**Important:** DO NOT delete or modify `backend/.env` file!

---

## 🎓 Demo Checklist for Professor

Before showing to professor:

✅ **Test Run (Night Before)**
- [ ] Extract ZIP and run setup
- [ ] Start application once to verify it works
- [ ] Test login with all 3 accounts
- [ ] Check that data loads correctly
- [ ] Verify internet connection works

✅ **Day of Demo**
- [ ] Close all other applications (save memory)
- [ ] Ensure stable internet connection
- [ ] Start application 5 minutes before demo
- [ ] Open browser to http://localhost:5173
- [ ] Verify dashboard loads with data
- [ ] Keep both terminal windows open (minimize them)

✅ **Demo Features to Show**
1. **Dashboard** with analytics and charts (opens automatically)
2. **Buildings & Units** management
3. **Tenants** list and details
4. **Maintenance Requests** - show status tracking
5. **Staff** assignments
6. **Create new request** (show form)
7. **Real-time updates** (status changes)
8. **Navigation** through sidebar menu

---

## 🐛 Troubleshooting

### Problem: "Python not found" or "Node not found"

**Solution:** Install Python 3.12+ and Node.js 18+ (see Step 1 & 2 above)

### Problem: Port 8000 or 5173 already in use

**Solution:**
```bash
# Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F

# Kill process on port 5173
netstat -ano | findstr :5173
taskkill /PID <PID_NUMBER> /F
```

### Problem: "Module not found" error

**Solution:**
```bash
cd backend
venv\Scripts\activate
pip install -r requirements.txt --force-reinstall
```

### Problem: Database connection error

**Check:**
1. ✅ Internet connection active?
2. ✅ `backend/.env` file exists?
3. ✅ Not behind firewall blocking AWS?

### Problem: npm install fails

**Solution:**
```bash
cd frontend
npm cache clean --force
rm -rf node_modules
npm install
```

### Problem: Virtual environment won't activate

**Solution:**
```bash
# Try this instead
venv\Scripts\activate.bat

# Or use full path
C:\path\to\project\backend\venv\Scripts\activate
```

### Problem: Browser shows "Cannot connect"

**Check:**
1. ✅ Both servers running? (check terminals)
2. ✅ Backend shows "Application startup complete"?
3. ✅ Frontend shows "Local: http://localhost:5173"?
4. ✅ Wait 20 seconds after starting

---

## 📞 Emergency Contact (Day of Demo)

If something breaks during setup:

1. **Check troubleshooting section above** (90% of issues solved here)
2. **Restart everything:**
   - Close both terminals
   - Double-click `start-demo.bat` again
   - Wait 30 seconds
3. **Verify Prerequisites:**
   - `python --version` (should show 3.12+)
   - `node --version` (should show 18+)
   - Internet connection active

---

## 🌐 URLs During Demo

- **Frontend:** http://localhost:5173
- **Backend API:** http://127.0.0.1:8000
- **API Documentation:** http://127.0.0.1:8000/docs
- **Database:** NEON Cloud (automatic connection)

---

## 📚 Additional Documentation

- **README.md** - Quick setup guide (this file but shorter)
- **DEPLOYMENT_README.md** - Detailed technical documentation
- **backend/requirements.txt** - All Python packages
- **frontend/package.json** - All Node packages

---

## 💡 Pro Tips

1. **Test before demo:** Run the application the night before to verify everything works
2. **Internet required:** Database is cloud-hosted (NEON)
3. **Keep terminals open:** Don't close the terminal windows while demo running
4. **Backup plan:** Take screenshots of working application in case of technical issues
5. **Demo data:** All data already loaded, no seeding required!

---

## 🎉 You're Ready!

**Time to Demo:** ~20 seconds (after setup)  
**Setup Status:** ✅ Complete  
**Database:** ✅ Populated  
**Code:** ✅ Ready

**Good luck with your demo!** 🚀

---

**Questions?** Check DEPLOYMENT_README.md for detailed technical information.
