# 📸 SCREENSHOT CHECKLIST FOR SUBMISSION
## Apartment Maintenance Request System - Milestone 2

**Date:** November 10, 2025  
**Your Application URLs:**
- Frontend: http://localhost:5173
- Backend: http://127.0.0.1:8000
- Backend Docs: http://127.0.0.1:8000/docs

---

## ✅ PRIORITY 1: APPLICATION SCREENSHOTS (MUST HAVE)

### 1️⃣ **Dashboard Overview** (Figure A4)
**URL:** http://localhost:5173
**What to show:**
- [ ] KPI Cards at top (Active Requests, Completed, Avg Resolution Time, SLA Breaches)
- [ ] Line chart showing requests over time
- [ ] Pie charts (by status, priority, issue type)
- Make sure data is visible and charts are rendered

**Tips:**
- Zoom out browser to 80-90% if needed to fit everything
- Wait for all charts to load before screenshot
- Use full browser window (not mobile view)

---

### 2️⃣ **Buildings List** (Figure A6)
**URL:** http://localhost:5173/buildings (or navigate to Buildings section)
**What to show:**
- [ ] Table with all 5 buildings
- [ ] Boston addresses visible (Back Bay, Beacon Hill, South End, North End, Fenway)
- [ ] Building names visible (Riverside Apartments, Sunset Tower, Harbor View, etc.)

---

### 3️⃣ **Maintenance Requests List** (Figure A8)
**URL:** http://localhost:5173/requests (or Requests section)
**What to show:**
- [ ] Table with multiple requests
- [ ] Status badges visible (Open, In Progress, Closed) in different colors
- [ ] Priority indicators visible
- [ ] Issue types visible (Plumbing, Electrical, HVAC, etc.)
- [ ] At least 10-15 rows visible

**Tips:**
- Scroll to show variety of statuses
- Make sure color-coded badges are visible

---

### 4️⃣ **Create New Request Form** (Figure A7)
**URL:** http://localhost:5173/requests/new (or click "Create Request" button)
**What to show:**
- [ ] Form fields visible: Tenant dropdown, Unit dropdown, Issue Type, Priority, Description
- [ ] Submit button visible
- [ ] Clean, professional form layout

---

### 5️⃣ **Request Details View** (Figure A9)
**URL:** Click on any request from the list
**What to show:**
- [ ] Full request information (ID, status, priority, description)
- [ ] Assignment section with staff member assigned
- [ ] Timestamps (created, updated, assigned, completed)
- [ ] Notes section with comments
- [ ] Building/Unit/Tenant information

**Tips:**
- Choose a request that has assignments and notes to show full functionality

---

### 6️⃣ **Staff List** (Optional but Good to Have)
**URL:** http://localhost:5173/staff
**What to show:**
- [ ] List of maintenance staff (Plumber, Electrician, HVAC Technician, etc.)
- [ ] Staff roles/specialties visible

---

### 7️⃣ **Tenants List** (Optional but Good to Have)
**URL:** http://localhost:5173/tenants
**What to show:**
- [ ] List of tenants with names and contact info
- [ ] Unit assignments visible

---

### 8️⃣ **Units List** (Optional but Good to Have)
**URL:** http://localhost:5173/units
**What to show:**
- [ ] List of units with unit numbers, floors, bedrooms
- [ ] Building references visible

---

## ✅ PRIORITY 2: DATABASE SCREENSHOTS (MUST HAVE)

### 9️⃣ **NEON PostgreSQL Console - Tables List** (Figure A1)
**URL:** https://console.neon.tech
**Login:** Use your NEON credentials
**What to show:**
- [ ] List of tables: buildings, units, tenants, staff, requests
- [ ] Table sizes or row counts visible
- [ ] Database name "neondb" visible at top

**How to get this:**
1. Go to https://console.neon.tech
2. Login with your account
3. Select your project
4. Go to "Tables" or "SQL Editor"
5. Run: `SELECT table_name, (SELECT COUNT(*) FROM table_name) as row_count FROM information_schema.tables WHERE table_schema='public';`
6. Screenshot the results

---

### 🔟 **Buildings Table Data** (Figure A2)
**In NEON SQL Editor, run:**
```sql
SELECT * FROM buildings LIMIT 5;
```
**What to show:**
- [ ] All 5 buildings with Boston addresses
- [ ] Neighborhoods: Back Bay, Beacon Hill, South End, North End, Fenway
- [ ] Building names visible

---

### 1️⃣1️⃣ **Requests Table with JSON Data** (Figure A3)
**In NEON SQL Editor, run:**
```sql
SELECT id, external_id, status, priority, issue_type, 
       assignments::text, notes::text 
FROM requests 
WHERE assignments IS NOT NULL AND notes IS NOT NULL
LIMIT 3;
```
**What to show:**
- [ ] Request records with complex JSON data visible
- [ ] Assignments column showing staff assignments
- [ ] Notes column showing tenant comments

---

## ✅ PRIORITY 3: DEVELOPMENT EVIDENCE (HIGHLY RECOMMENDED)

### 1️⃣2️⃣ **VS Code Terminal - Database Seeding Success** (Figure A10)
**Already captured! Check your terminal history**
**What to show:**
```
✅ Created 5 buildings
✅ Created 200 units
✅ Created 100 tenants
✅ Created 5 staff members
✅ Created 200 requests
🎉 Database seeding completed successfully!
```

**How to capture:**
- Scroll up in your PowerShell terminal to find this output
- Screenshot the entire output section
- OR re-run: `cd backend ; python seed_pg_data.py`

---

### 1️⃣3️⃣ **Backend Running - PostgreSQL Connection** (Figure A12)
**Your backend terminal should show:**
```
Connected to PostgreSQL: neondb
INFO: Application startup complete.
INFO: Uvicorn running on http://127.0.0.1:8000
```

**How to capture:**
- Check the terminal where you ran `uvicorn app.main:app --reload`
- Scroll to the top where it connected to database
- Screenshot showing successful connection

---

### 1️⃣4️⃣ **API Documentation Page** (Bonus)
**URL:** http://127.0.0.1:8000/docs
**What to show:**
- [ ] Swagger UI with all API endpoints listed
- [ ] Routers visible: buildings, units, tenants, staff, requests, metrics
- [ ] Shows professional API structure

---

### 1️⃣5️⃣ **API Response Example** (Figure A11)
**URL:** http://127.0.0.1:8000/buildings
**What to show:**
- [ ] JSON response in browser showing all 5 buildings
- [ ] Well-formatted JSON with building data

**How to capture:**
1. Open browser
2. Go to http://127.0.0.1:8000/buildings
3. Browser will display JSON
4. Screenshot the JSON response

**OR use Swagger UI:**
1. Go to http://127.0.0.1:8000/docs
2. Find GET /buildings endpoint
3. Click "Try it out"
4. Click "Execute"
5. Screenshot the response

---

## ✅ OPTIONAL BUT IMPRESSIVE

### 1️⃣6️⃣ **Browser DevTools Network Tab**
**Shows API calls being made:**
- [ ] Open DevTools (F12)
- [ ] Go to Network tab
- [ ] Refresh page
- [ ] Show successful API calls (200 status codes)

---

### 1️⃣7️⃣ **VS Code Project Structure**
**Shows your codebase organization:**
- [ ] File explorer showing backend/ and frontend/ folders
- [ ] Key files visible: main.py, database.py, models/, routers/

---

## 📋 SCREENSHOT NAMING CONVENTION

Save your screenshots with clear names:
- `Figure_A1_NEON_Tables_List.png`
- `Figure_A2_Buildings_Data.png`
- `Figure_A3_Requests_JSON.png`
- `Figure_A4_Dashboard_Overview.png`
- `Figure_A5_Analytics_Charts.png`
- `Figure_A6_Buildings_List.png`
- `Figure_A7_Create_Request_Form.png`
- `Figure_A8_Requests_List.png`
- `Figure_A9_Request_Details.png`
- `Figure_A10_Database_Seeding.png`
- `Figure_A11_API_Response.png`
- `Figure_A12_Backend_Connected.png`

---

## 🎯 QUALITY TIPS

✅ **DO:**
- Use high resolution (1920x1080 or higher)
- Make sure text is readable
- Show full window (not cropped awkwardly)
- Ensure data is loaded before screenshot
- Use light theme if possible (prints better)
- Include browser address bar to show URL

❌ **DON'T:**
- Use low resolution or blurry images
- Crop important information
- Screenshot while page is loading
- Include personal information (if any)
- Use dark mode (harder to print)

---

## 📊 QUICK REFERENCE: WHAT EACH SCREENSHOT PROVES

| Figure | What It Proves | Points Covered |
|--------|----------------|----------------|
| A1 | Database exists with correct tables | Database Creation (4a) |
| A2-A3 | Sample data loaded successfully | Data Loading (4a) |
| A4-A5 | Analytical queries work + Visualization | Analytics & Viz (4c) |
| A6-A9 | CRUD operations work through UI | Application Functionality |
| A10 | Database initialization successful | Technical Evidence |
| A11 | API returns data from PostgreSQL | Backend Integration |
| A12 | Backend connected to cloud database | Cloud Database Setup |

---

## ⏰ TIME ESTIMATE

**Total time needed:** 20-30 minutes

**Priority 1 Screenshots:** 15 minutes (Application)
**Priority 2 Screenshots:** 10 minutes (Database)
**Priority 3 Screenshots:** 5 minutes (Development)

---

## 🚀 READY TO START?

**Step 1:** Make sure both servers are running:
- Backend: ✅ http://127.0.0.1:8000
- Frontend: ✅ http://localhost:5173

**Step 2:** Open this checklist on one screen, browser on another

**Step 3:** Go through each screenshot systematically

**Step 4:** Save with descriptive names

**Step 5:** Insert into your Word document using FINAL_SUBMISSION_GUIDE.md

---

## 📞 NEED HELP?

If any page doesn't load:
1. Check both servers are running
2. Check browser console for errors (F12)
3. Try refreshing the page
4. Check network tab to see if API calls are failing

---

**You've got this! Your system is working perfectly - now just capture the evidence! 📸✨**
