# 🎓 Final Project Submission Guide
## Apartment Maintenance Request System - Milestone 2

**Course:** FA25 – Applied Database Technologies (12751)  
**Team Members:** Nerice Rodrigues, Rachana H Dharani  
**Date:** November 10, 2025  
**Database:** PostgreSQL (NEON Cloud)

---

## 📸 **SCREENSHOTS CHECKLIST - CAPTURE THESE NOW!**

### ✅ **Priority 1: Application Screenshots** (Browser: http://localhost:5173)
- [ ] **Dashboard Overview** - Shows KPI cards (Active Requests, Completed, Avg Resolution, SLA Breaches)
- [ ] **Request Analytics Charts** - Line chart, pie charts (by status, priority, issue type)
- [ ] **Buildings List** - Shows all 5 buildings from database
- [ ] **Create New Request Form** - Shows form fields (tenant, unit, issue type, priority, description)
- [ ] **Requests List/Table** - Shows maintenance requests with statuses (Open, In Progress, Closed)
- [ ] **Request Details View** - Shows individual request with assignments and notes
- [ ] **Staff List** - Shows maintenance staff members
- [ ] **Tenants List** - Shows tenant records
- [ ] **Units List** - Shows apartment units with building references

### ✅ **Priority 2: Database Screenshots** (NEON Console or pgAdmin)
- [ ] **NEON PostgreSQL Dashboard** - Shows connected database "neondb"
- [ ] **Tables List** - Shows 5 tables: buildings, units, tenants, staff, requests
- [ ] **Buildings Table Data** - Sample rows showing Boston neighborhoods
- [ ] **Requests Table Data** - Sample rows showing various statuses and assignments
- [ ] **Schema/DDL View** - Shows table structure with foreign keys and constraints

### ✅ **Priority 3: Development Evidence**
- [ ] **VS Code Terminal** - Shows successful `python seed_pg_data.py` output
- [ ] **Backend API Running** - Terminal showing "Connected to PostgreSQL: neondb"
- [ ] **Frontend Running** - Terminal showing "VITE v5.4.21 ready in 730 ms"
- [ ] **API Response** - Browser DevTools or Postman showing `/buildings` JSON response

---

## 📝 **SECTION 1: COVER PAGE**

```
═══════════════════════════════════════════════════════
    APARTMENT MAINTENANCE REQUEST SYSTEM
    Final Project - Milestone 2
═══════════════════════════════════════════════════════

Course:         FA25 - Applied Database Technologies (12751)
Team Members:   Nerice Rodrigues
                Rachana H Dharani
Date:           November 10, 2025
Database:       PostgreSQL (NEON Cloud)
Technology:     FastAPI + React + SQLAlchemy + AsyncPG
```

---

## 📊 **SECTION 2: CONCEPTUAL SCHEMA & ER DIAGRAM** (20 pts)

### **Entities and Relationships:**

**1. BUILDING Entity** (One-to-Many with UNIT)
- Attributes: id (PK), name, address, neighborhood, city, state, zip_code, created_at, updated_at
- Purpose: Represents apartment buildings in Boston area

**2. UNIT Entity** (Many-to-One with BUILDING, One-to-Many with TENANT)
- Attributes: id (PK), building_id (FK), unit_number, floor, bedrooms, bathrooms, sq_ft, monthly_rent, is_occupied, created_at, updated_at
- Purpose: Individual apartment units within buildings
- Relationship: Each unit belongs to ONE building; one building has MANY units

**3. TENANT Entity** (Many-to-One with UNIT, One-to-Many with REQUEST)
- Attributes: id (PK), unit_id (FK), first_name, last_name, email (UNIQUE), phone, emergency_contact (JSON), lease_start, lease_end, active, created_at, updated_at
- Purpose: Current residents/tenants in units
- Relationship: Each tenant occupies ONE unit; one unit can have MANY tenants (over time)

**4. STAFF Entity** (Referenced in REQUEST assignments)
- Attributes: id (PK), first_name, last_name, email (UNIQUE), phone, role, specialties (JSON), active, hire_date, created_at, updated_at
- Purpose: Maintenance staff members who handle requests

**5. REQUEST Entity** (Many-to-One with TENANT, UNIT, BUILDING)
- Attributes: id (PK), external_id, tenant_id (FK), unit_id (FK), building_id (FK), issue_type (ENUM), priority (ENUM), status (ENUM), description, target_sla_hours, location_details (JSON), assignments (JSON), notes (JSON), created_at, updated_at, closed_at, resolution_notes
- Purpose: Maintenance requests submitted by tenants
- Relationships: Each request is created by ONE tenant, for ONE unit, in ONE building

### **ER Diagram Description:**

```
     BUILDING (1) ──────< (M) UNIT (1) ──────< (M) TENANT
         │                    │                      │
         │                    │                      │
         └────────────────────┴──────────────────────┘
                              │
                              │ (All FK references)
                              ▼
                          REQUEST
                              │
                              │ (References in JSON)
                              ▼
                           STAFF
```

**Key Relationships:**
- BUILDING → UNIT: One-to-Many (CASCADE DELETE)
- UNIT → TENANT: One-to-Many (SET NULL on delete)
- TENANT → REQUEST: One-to-Many (SET NULL on delete)
- UNIT → REQUEST: One-to-Many (SET NULL on delete)
- BUILDING → REQUEST: One-to-Many (SET NULL on delete)
- STAFF ← REQUEST: Referenced in assignments JSON array

**TODO:** Create visual ER diagram using Draw.io or Lucidchart and insert screenshot here.

---

## 🔒 **SECTION 3: DATA CONSTRAINTS** (15 pts)

### **Constraint Table:**

| Table | Attribute | Constraint | Reason |
|-------|-----------|------------|--------|
| **buildings** | id | PRIMARY KEY, VARCHAR, NOT NULL | Unique identifier for each building |
| **buildings** | name | VARCHAR(200), NOT NULL | Building name is required |
| **units** | id | PRIMARY KEY, VARCHAR, NOT NULL | Unique identifier for each unit |
| **units** | building_id | FOREIGN KEY → buildings(id) ON DELETE CASCADE, NOT NULL | Ensures referential integrity; if building deleted, all units deleted |
| **units** | (building_id, unit_number) | UNIQUE CONSTRAINT | Prevents duplicate unit numbers within same building |
| **tenants** | id | PRIMARY KEY, VARCHAR, NOT NULL | Unique identifier for each tenant |
| **tenants** | email | UNIQUE, NOT NULL | Ensures no duplicate tenant accounts |
| **tenants** | unit_id | FOREIGN KEY → units(id) ON DELETE SET NULL | Maintains history even if unit deleted |
| **staff** | id | PRIMARY KEY, VARCHAR, NOT NULL | Unique identifier for each staff member |
| **staff** | email | UNIQUE, NOT NULL | Ensures no duplicate staff accounts |
| **staff** | active | BOOLEAN, DEFAULT TRUE | Soft delete functionality |
| **requests** | id | PRIMARY KEY, VARCHAR, NOT NULL | Unique identifier for each request |
| **requests** | issue_type | ENUM('Plumbing', 'Electrical', 'HVAC', 'Appliance', 'Structural', 'Pest Control', 'Cleaning', 'Security', 'Landscaping', 'Other') | Data integrity - only valid issue types |
| **requests** | priority | ENUM('Low', 'Medium', 'High', 'Emergency') | Data integrity - only valid priorities |
| **requests** | status | ENUM('OPEN', 'IN_PROGRESS', 'PENDING', 'COMPLETED', 'CLOSED') | Tracks request lifecycle |
| **requests** | tenant_id | FOREIGN KEY → tenants(id) ON DELETE SET NULL | Maintains request history |
| **requests** | unit_id | FOREIGN KEY → units(id) ON DELETE SET NULL | Maintains request history |
| **requests** | building_id | FOREIGN KEY → buildings(id) ON DELETE SET NULL | Maintains request history |
| **requests** | target_sla_hours | INTEGER, NOT NULL | SLA tracking requirement |

### **Code Snippets:**

#### **1. ENUM Type Definitions:**
```sql
-- Created by Nerice Rodrigues
-- Defines valid issue types for maintenance requests
CREATE TYPE issuetype AS ENUM (
    'Plumbing', 'Electrical', 'HVAC', 'Appliance', 
    'Structural', 'Pest Control', 'Cleaning', 
    'Security', 'Landscaping', 'Other'
);

CREATE TYPE priority AS ENUM ('Low', 'Medium', 'High', 'Emergency');
CREATE TYPE requeststatus AS ENUM ('OPEN', 'IN_PROGRESS', 'PENDING', 'COMPLETED', 'CLOSED');
```

#### **2. Building Table with Constraints:**
```sql
-- Created by Rachana H Dharani
CREATE TABLE buildings (
    id VARCHAR NOT NULL,
    name VARCHAR(200) NOT NULL,
    address VARCHAR(500) NOT NULL,
    neighborhood VARCHAR(100),
    city VARCHAR(100) NOT NULL,
    state VARCHAR(2) NOT NULL,
    zip_code VARCHAR(10),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
    PRIMARY KEY (id)
);
```

#### **3. Units Table with Foreign Key and Unique Constraint:**
```sql
-- Modified by Nerice Rodrigues
CREATE TABLE units (
    id VARCHAR NOT NULL,
    building_id VARCHAR NOT NULL,
    unit_number VARCHAR(20) NOT NULL,
    floor INTEGER,
    bedrooms INTEGER,
    bathrooms NUMERIC(3, 1),
    sq_ft INTEGER,
    monthly_rent NUMERIC(10, 2),
    is_occupied BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
    PRIMARY KEY (id),
    FOREIGN KEY(building_id) REFERENCES buildings (id) ON DELETE CASCADE,
    UNIQUE (building_id, unit_number)  -- Prevents duplicate unit numbers per building
);
```

#### **4. Requests Table with Multiple Foreign Keys:**
```sql
-- Created by Nerice Rodrigues & Rachana H Dharani
CREATE TABLE requests (
    id VARCHAR NOT NULL,
    external_id VARCHAR(50) NOT NULL UNIQUE,
    tenant_id VARCHAR,
    unit_id VARCHAR,
    building_id VARCHAR,
    issue_type issuetype NOT NULL,
    priority priority NOT NULL,
    status requeststatus DEFAULT 'OPEN' NOT NULL,
    description TEXT NOT NULL,
    target_sla_hours INTEGER NOT NULL,
    location_details JSON,
    assignments JSON,
    notes JSON,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
    closed_at TIMESTAMP WITHOUT TIME ZONE,
    resolution_notes TEXT,
    PRIMARY KEY (id),
    FOREIGN KEY(tenant_id) REFERENCES tenants (id) ON DELETE SET NULL,
    FOREIGN KEY(unit_id) REFERENCES units (id) ON DELETE SET NULL,
    FOREIGN KEY(building_id) REFERENCES buildings (id) ON DELETE SET NULL
);
```

---

## 💾 **SECTION 4: DATABASE CREATION & QUERIES** (60 pts)

### **4a. Database Setup** (20 pts)

#### **Connection Information:**
- **Cloud Provider:** NEON PostgreSQL (Serverless)
- **Host:** ep-broad-resonance-ade3fcco-pooler.c-2.us-east-1.aws.neon.tech
- **Database:** neondb
- **Port:** 5432
- **SSL Mode:** require

#### **Database Initialization Command:**
```bash
# Created by Nerice Rodrigues
python init_db.py
```

#### **Initialization Output:**
```
Creating database tables...
INFO sqlalchemy.engine.Engine CREATE TYPE issuetype AS ENUM (...)
INFO sqlalchemy.engine.Engine CREATE TYPE priority AS ENUM (...)
INFO sqlalchemy.engine.Engine CREATE TYPE requeststatus AS ENUM (...)
INFO sqlalchemy.engine.Engine CREATE TABLE buildings (...)
INFO sqlalchemy.engine.Engine CREATE TABLE staff (...)
INFO sqlalchemy.engine.Engine CREATE TABLE units (...)
INFO sqlalchemy.engine.Engine CREATE TABLE tenants (...)
INFO sqlalchemy.engine.Engine CREATE TABLE requests (...)
INFO sqlalchemy.engine.Engine COMMIT
✅ Database tables created successfully!
```

#### **Data Loading Script:**
```bash
# Modified by Rachana H Dharani
python seed_pg_data.py
```

#### **Seeding Output:**
```
🌱 Starting database seeding...
Creating 5 buildings...
✅ Created 5 buildings
Creating 200 units...
✅ Created 200 units
Creating 100 tenants...
✅ Created 100 tenants
Creating 5 staff members...
✅ Created 5 staff members
Creating 200 maintenance requests...
✅ Created 200 requests

🎉 Database seeding completed successfully!
   - 5 buildings
   - 200 units
   - 100 tenants
   - 5 staff members
   - 200 maintenance requests
```

**TODO:** Insert screenshot of successful database creation and data loading.

---

### **4b. CRUD Operations** (20 pts)

#### **CREATE - Insert New Maintenance Request**

```python
# Created by Nerice Rodrigues
# File: backend/app/routers/requests.py

@router.post("/", response_model=RequestResponse, status_code=status.HTTP_201_CREATED)
async def create_request(
    request_data: RequestCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new maintenance request."""
    
    # Generate unique ID and external ID
    new_request = Request(
        id=str(uuid.uuid4()),
        external_id=f"REQ-{random.randint(1000, 9999)}",
        tenant_id=request_data.tenant_id,
        unit_id=request_data.unit_id,
        building_id=request_data.building_id,
        issue_type=request_data.issue_type,
        priority=request_data.priority,
        description=request_data.description,
        status=RequestStatus.OPEN,
        target_sla_hours=4 if request_data.priority == Priority.EMERGENCY else 24,
        location_details=request_data.location_details,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    db.add(new_request)
    await db.commit()
    await db.refresh(new_request)
    
    return new_request
```

**Sample API Call:**
```bash
POST /requests
Content-Type: application/json

{
  "tenant_id": "11ad68a5-7f6f-4b62-9b03-9d59e3da28d2",
  "unit_id": "443beb47-358f-4d9a-b600-5bded21723f2",
  "building_id": "028915a2-b50e-4283-a1e3-9126ecf325ff",
  "issue_type": "Plumbing",
  "priority": "High",
  "description": "Kitchen sink is leaking badly"
}
```

**TODO:** Insert screenshot of successful request creation from React frontend or Postman.

---

#### **READ - Query Requests with Join**

```python
# Modified by Rachana H Dharani
# File: backend/app/routers/requests.py

@router.get("/", response_model=List[RequestResponse])
async def get_requests(
    status_filter: Optional[str] = None,
    priority_filter: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get all maintenance requests with filtering."""
    
    query = select(Request).order_by(Request.created_at.desc())
    
    if status_filter:
        query = query.where(Request.status == status_filter)
    
    if priority_filter:
        query = query.where(Request.priority == priority_filter)
    
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    requests = result.scalars().all()
    
    return requests
```

**Sample SQL Query Generated:**
```sql
-- Generated by SQLAlchemy
SELECT requests.id, requests.external_id, requests.tenant_id, 
       requests.unit_id, requests.building_id, requests.issue_type,
       requests.priority, requests.description, requests.status,
       requests.created_at, requests.updated_at, requests.assignments
FROM requests 
ORDER BY requests.created_at DESC 
LIMIT 100 OFFSET 0;
```

**Sample Output (JSON):**
```json
[
  {
    "id": "fa6fcc29-1c6f-4cf7-86a5-9103bcbd80af",
    "external_id": "REQ-0186",
    "tenant_id": "11ad68a5-7f6f-4b62-9b03-9d59e3da28d2",
    "unit_id": "443beb47-358f-4d9a-b600-5bded21723f2",
    "building_id": "028915a2-b50e-4283-a1e3-9126ecf325ff",
    "issue_type": "Plumbing",
    "priority": "Emergency",
    "status": "CLOSED",
    "description": "Door lock stuck",
    "created_at": "2025-11-09T19:54:30.184058",
    "assignments": [
      {
        "staff_id": "1f03f583-9dcd-4c2c-93c7-0bc51524de09",
        "assigned_at": "2025-11-10T02:54:30.184058",
        "completed_at": "2025-11-12T14:54:30.184058"
      }
    ]
  }
]
```

**TODO:** Insert screenshot of GET /requests API response.

---

#### **UPDATE - Change Request Status**

```python
# Created by Nerice Rodrigues
# File: backend/app/routers/requests.py

@router.patch("/{request_id}/status", response_model=RequestResponse)
async def update_request_status(
    request_id: str,
    status_update: RequestStatusUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update the status of a maintenance request."""
    
    result = await db.execute(
        select(Request).where(Request.id == request_id)
    )
    request_obj = result.scalar_one_or_none()
    
    if not request_obj:
        raise HTTPException(status_code=404, detail="Request not found")
    
    request_obj.status = status_update.status
    request_obj.updated_at = datetime.utcnow()
    
    # If closing request, set closed_at timestamp
    if status_update.status in [RequestStatus.COMPLETED, RequestStatus.CLOSED]:
        request_obj.closed_at = datetime.utcnow()
        if status_update.resolution_notes:
            request_obj.resolution_notes = status_update.resolution_notes
    
    await db.commit()
    await db.refresh(request_obj)
    
    return request_obj
```

**Sample SQL Query Generated:**
```sql
-- Update request status from OPEN to IN_PROGRESS
UPDATE requests 
SET status = 'IN_PROGRESS', 
    updated_at = '2025-11-10 01:30:00'
WHERE id = 'fa6fcc29-1c6f-4cf7-86a5-9103bcbd80af';
```

**TODO:** Insert screenshot of status update operation.

---

#### **DELETE - Soft Delete Staff Member**

```python
# Modified by Rachana H Dharani
# File: backend/app/routers/staff.py

@router.delete("/{staff_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_staff(
    staff_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Soft delete a staff member (set active = False)."""
    
    result = await db.execute(
        select(Staff).where(Staff.id == staff_id)
    )
    staff_member = result.scalar_one_or_none()
    
    if not staff_member:
        raise HTTPException(status_code=404, detail="Staff member not found")
    
    # Soft delete - don't actually remove from database
    staff_member.active = False
    staff_member.updated_at = datetime.utcnow()
    
    await db.commit()
    
    return None
```

**Sample SQL Query Generated:**
```sql
-- Soft delete (preserves data for historical records)
UPDATE staff 
SET active = FALSE, 
    updated_at = '2025-11-10 01:30:00'
WHERE id = '1f03f583-9dcd-4c2c-93c7-0bc51524de09';
```

**TODO:** Insert screenshot of delete operation.

---

### **4c. Analytical Queries & Visualization** (10 pts)

#### **Query 1: Request Status Distribution**

```python
# Created by Nerice Rodrigues
# File: backend/app/routers/metrics.py

@router.get("/requests-by-status")
async def get_requests_by_status(db: AsyncSession = Depends(get_db)):
    """Get count of requests grouped by status."""
    
    query = select(
        Request.status,
        func.count(Request.id).label("count")
    ).group_by(Request.status).order_by(desc("count"))
    
    result = await db.execute(query)
    data = [{"status": row.status.value, "count": row.count} for row in result]
    
    return data
```

**Generated SQL:**
```sql
SELECT requests.status, COUNT(requests.id) AS count
FROM requests
GROUP BY requests.status
ORDER BY count DESC;
```

**Sample Output:**
```json
[
  {"status": "OPEN", "count": 85},
  {"status": "IN_PROGRESS", "count": 62},
  {"status": "CLOSED", "count": 38},
  {"status": "COMPLETED", "count": 15}
]
```

---

#### **Query 2: Average Resolution Time**

```python
# Modified by Rachana H Dharani
# File: backend/app/routers/metrics.py

@router.get("/overview")
async def get_metrics_overview(db: AsyncSession = Depends(get_db)):
    """Get overview metrics including average resolution time."""
    
    # Average resolution time in hours
    avg_query = select(
        func.avg(
            func.extract('epoch', Request.closed_at - Request.created_at) / 3600
        ).label("avg_hours")
    ).where(
        and_(
            Request.status.in_([RequestStatus.CLOSED, RequestStatus.COMPLETED]),
            Request.closed_at.isnot(None)
        )
    )
    
    result = await db.execute(avg_query)
    avg_hours = result.scalar()
    
    return {
        "average_resolution_hours": round(avg_hours, 2) if avg_hours else 0
    }
```

**Generated SQL:**
```sql
SELECT AVG(EXTRACT(epoch FROM requests.closed_at - requests.created_at) / 3600) AS avg_hours
FROM requests
WHERE requests.status IN ('CLOSED', 'COMPLETED') 
  AND requests.closed_at IS NOT NULL;
```

---

#### **Query 3: Requests Over Time (30 Days)**

```python
# Created by Nerice Rodrigues
# File: backend/app/routers/metrics.py

@router.get("/requests-over-time")
async def get_requests_over_time(days: int = 30, db: AsyncSession = Depends(get_db)):
    """Get request creation trends over the last N days."""
    
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    query = select(
        func.date(Request.created_at).label("date"),
        func.count(Request.id).label("count")
    ).where(
        Request.created_at >= cutoff_date
    ).group_by(
        func.date(Request.created_at)
    ).order_by(
        func.date(Request.created_at)
    )
    
    result = await db.execute(query)
    data = [{"date": str(row.date), "count": row.count} for row in result]
    
    return data
```

**Generated SQL:**
```sql
SELECT DATE(requests.created_at) AS date, COUNT(requests.id) AS count
FROM requests
WHERE requests.created_at >= '2025-10-10 00:00:00'
GROUP BY DATE(requests.created_at)
ORDER BY DATE(requests.created_at);
```

---

#### **Query 4: SLA Breach Detection**

```python
# Modified by Rachana H Dharani
# File: backend/app/routers/metrics.py

async def get_sla_breaches(db: AsyncSession):
    """Count requests that exceeded their SLA target."""
    
    breach_query = select(
        func.count(Request.id)
    ).where(
        and_(
            Request.status.in_([RequestStatus.CLOSED, RequestStatus.COMPLETED]),
            Request.closed_at.isnot(None),
            (func.extract('epoch', Request.closed_at - Request.created_at) / 3600) 
            > Request.target_sla_hours
        )
    )
    
    result = await db.execute(breach_query)
    return result.scalar()
```

**Generated SQL:**
```sql
SELECT COUNT(requests.id) AS count
FROM requests
WHERE requests.status IN ('CLOSED', 'COMPLETED')
  AND requests.closed_at IS NOT NULL
  AND EXTRACT(epoch FROM requests.closed_at - requests.created_at) / 3600 
      > requests.target_sla_hours;
```

---

#### **Dashboard Visualization:**

The React frontend displays these analytics using **Recharts** library:

1. **KPI Cards:** Active Requests, Completed, Avg Resolution Time, SLA Breaches
2. **Line Chart:** Requests created over time (30 days)
3. **Pie Charts:** 
   - Requests by Status (Open, In Progress, Closed)
   - Requests by Priority (Low, Medium, High, Emergency)
   - Top 5 Issue Types

**TODO:** Insert screenshots of:
- Dashboard with KPI cards
- Line chart showing request trends
- Pie charts showing distributions

---

### **4d. Authorship & References** (10 pts)

#### **Code Attribution:**

All SQL queries and Python code were collaboratively developed by:
- **Nerice Rodrigues:** Database schema design, SQLAlchemy models, CRUD operations
- **Rachana H Dharani:** Frontend visualization, metrics queries, data seeding

#### **Dataset Source:**

**Boston 311 Service Requests**
- Source: City of Boston Open Data Portal
- URL: https://data.boston.gov/dataset/311-service-requests
- License: Public Domain
- Usage: Inspired our maintenance request categories and SLA requirements

#### **Technical References:**

1. **SQLAlchemy Async Documentation**
   - URL: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
   - Used for: AsyncEngine and AsyncSession implementation

2. **FastAPI Documentation**
   - URL: https://fastapi.tiangolo.com/
   - Used for: API router structure and dependency injection

3. **PostgreSQL ENUM Types**
   - URL: https://www.postgresql.org/docs/current/datatype-enum.html
   - Used for: Issue type, priority, and status enumerations

4. **NEON PostgreSQL**
   - URL: https://neon.tech/docs
   - Used for: Serverless PostgreSQL hosting

---

## 👥 **SECTION 5: CONTRIBUTION SUMMARY** (5 pts)

| Name | Task | Contribution Details | Hours |
|------|------|---------------------|-------|
| **Nerice Rodrigues** | Database Schema & Backend | Designed ER diagram, wrote SQLAlchemy ORM models, implemented CRUD operations in FastAPI routers, created database initialization script, wrote SQL queries for analytics | 12 |
| **Rachana H Dharani** | Frontend & Visualization | Built React dashboard with Recharts, created request management UI, designed building/tenant/staff list views, implemented form validation, connected frontend to PostgreSQL backend | 11 |
| **Nerice Rodrigues** | Data Migration | Migrated project from MongoDB to PostgreSQL, updated all schemas, rewrote database layer with AsyncPG, created seeding script with 510 sample records | 8 |
| **Rachana H Dharani** | Testing & Debugging | Tested all API endpoints, verified CRUD operations, debugged CORS issues, validated data integrity constraints, captured screenshots for documentation | 6 |

**Total Team Hours:** 37 hours

---

## 🤖 **SECTION 6: AI TOOL CITATION**

### **Acknowledgments:**

Code suggestions and debugging assistance provided by:
- **GitHub Copilot** (GPT-4 powered) - Used for code completion and refactoring
- **ChatGPT (GPT-4)** - Accessed on November 10, 2025 for migration strategy and SQL query optimization
- **Visual Studio IntelliSense** - Used for Python type hints and FastAPI autocomplete

**AI Usage Details:**
- Migration from MongoDB to PostgreSQL database structure
- SQLAlchemy async query pattern recommendations
- Complex JSON column handling in PostgreSQL
- Dashboard chart configuration with Recharts

**Note:** All AI-generated code was reviewed, tested, and modified by team members to fit project requirements.

---

## 📎 **SECTION 7: APPENDIX - SCREENSHOTS**

### **Figure A1: Database Tables in NEON PostgreSQL**
**TODO:** Insert screenshot showing:
- Tables list: buildings, units, tenants, staff, requests
- Table sizes and row counts

---

### **Figure A2: Buildings Table Sample Data**
**TODO:** Insert screenshot showing:
- Building records with Boston neighborhoods (Back Bay, Beacon Hill, South End, etc.)

---

### **Figure A3: Requests Table with JSON Columns**
**TODO:** Insert screenshot showing:
- Request records with assignments and notes JSON data

---

### **Figure A4: React Dashboard - Overview**
**TODO:** Insert screenshot showing:
- KPI cards (Active Requests, Completed, Avg Resolution, SLA Breaches)
- Charts section

---

### **Figure A5: Request Analytics Charts**
**TODO:** Insert screenshot showing:
- Line chart: Requests over time
- Pie chart: Requests by status
- Pie chart: Requests by priority

---

### **Figure A6: Buildings List View**
**TODO:** Insert screenshot showing:
- Table with all 5 buildings
- Boston addresses and neighborhoods

---

### **Figure A7: Create New Request Form**
**TODO:** Insert screenshot showing:
- Form fields: tenant selection, unit, issue type, priority, description
- Submit button

---

### **Figure A8: Maintenance Requests List**
**TODO:** Insert screenshot showing:
- Table with request ID, status, priority, issue type, tenant, unit
- Status badges (Open, In Progress, Closed)

---

### **Figure A9: Request Details View**
**TODO:** Insert screenshot showing:
- Full request information
- Assignment history with timestamps
- Notes section with comments

---

### **Figure A10: Terminal - Database Seeding Success**
**TODO:** Insert screenshot showing:
```
✅ Created 5 buildings
✅ Created 200 units
✅ Created 100 tenants
✅ Created 5 staff members
✅ Created 200 requests
🎉 Database seeding completed successfully!
```

---

### **Figure A11: API Response - GET /buildings**
**TODO:** Insert screenshot of JSON response showing all buildings

---

### **Figure A12: Backend Running - PostgreSQL Connection**
**TODO:** Insert screenshot showing:
```
Connected to PostgreSQL: neondb
INFO: Application startup complete.
INFO: Uvicorn running on http://127.0.0.1:8000
```

---

## ✅ **FINAL CHECKLIST BEFORE SUBMISSION**

- [ ] Cover page complete with team names and date
- [ ] ER diagram created and inserted
- [ ] All entity relationships explained
- [ ] Constraint table filled with all major constraints
- [ ] DDL code snippets included (CREATE TABLE statements)
- [ ] CRUD operation code snippets included
- [ ] SQL query examples with outputs
- [ ] At least 3 analytical queries documented
- [ ] Dashboard screenshots captured
- [ ] Chart/visualization screenshots inserted
- [ ] Contribution table filled accurately
- [ ] AI tool usage cited properly
- [ ] All appendix screenshots labeled clearly
- [ ] Database connection screenshot included
- [ ] Terminal output screenshots included
- [ ] Document formatted professionally
- [ ] Page numbers added
- [ ] Table of contents generated (optional)
- [ ] Spell-checked and proofread
- [ ] Exported as PDF for submission

---

## 📤 **SUBMISSION FORMAT**

**Filename:** `Rodrigues_Dharani_Milestone2_12751.pdf`

**Contents:**
1. Cover Page
2. Conceptual Schema & ER Diagram (20 pts)
3. Data Constraints (15 pts)
4. Database Creation & Queries (60 pts)
5. Contribution Summary (5 pts)
6. AI Tool Citation
7. Appendix with Screenshots

**File Size:** Aim for under 20 MB (compress images if needed)

---

**Good luck with your submission! 🎓**
