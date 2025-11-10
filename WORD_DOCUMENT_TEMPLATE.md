# WORD DOCUMENT TEMPLATE - COPY THIS STRUCTURE
## Use this as your Word document outline

---

# APARTMENT MAINTENANCE REQUEST SYSTEM
## Final Project - Milestone 2

**Course:** FA25 – Applied Database Technologies (12751)  
**Team Members:** Nerice Rodrigues, Rachana H Dharani  
**Date:** November 10, 2025  
**Database:** PostgreSQL (NEON Cloud)  
**Technology Stack:** FastAPI + React + SQLAlchemy + AsyncPG

---

## TABLE OF CONTENTS

1. Cover Page
2. Conceptual Schema & ER Diagram (20 pts)
3. Data Constraints (15 pts)
4. Database Creation & Queries (60 pts)
5. Contribution Summary (5 pts)
6. AI Tool Citation
7. Appendix - Screenshots

---

# 2. CONCEPTUAL SCHEMA & ER DIAGRAM (20 pts)

## 2.1 Database Overview

Our Apartment Maintenance Request System manages maintenance operations for multi-unit residential buildings. The database tracks buildings, units, tenants, staff members, and maintenance requests with their complete lifecycle from creation to resolution.

## 2.2 Entity Descriptions

### BUILDING Entity
Represents apartment buildings in the Boston area. Each building contains multiple units and is identified by a unique ID.

**Attributes:**
- id (PK): Unique identifier
- name: Building name (e.g., "Riverside Apartments")
- address: Street address
- neighborhood: Boston neighborhood (Back Bay, Beacon Hill, etc.)
- city, state, zip_code: Location details
- created_at, updated_at: Audit timestamps

**Purpose:** Central entity that groups units and provides geographical context for maintenance requests.

---

### UNIT Entity
Represents individual apartment units within buildings. Each unit belongs to exactly one building and can be occupied by tenants.

**Attributes:**
- id (PK): Unique identifier
- building_id (FK): Reference to parent building
- unit_number: Unit identifier within building (e.g., "204")
- floor: Floor number
- bedrooms, bathrooms: Unit specifications
- sq_ft: Square footage
- monthly_rent: Rental amount
- is_occupied: Occupancy status
- created_at, updated_at: Audit timestamps

**Purpose:** Links buildings to tenants and provides physical location context for maintenance requests.

**Constraint:** UNIQUE (building_id, unit_number) - Prevents duplicate unit numbers within same building.

---

### TENANT Entity
Represents residents who occupy units and submit maintenance requests. Each tenant is assigned to one unit at a time.

**Attributes:**
- id (PK): Unique identifier
- unit_id (FK): Reference to occupied unit
- first_name, last_name: Tenant name
- email (UNIQUE): Contact email
- phone: Contact phone
- emergency_contact (JSON): Emergency contact information
- lease_start, lease_end: Lease period
- active: Current status
- created_at, updated_at: Audit timestamps

**Purpose:** Represents requestors in the system and links maintenance issues to responsible parties.

---

### STAFF Entity
Represents maintenance personnel who handle and complete maintenance requests. Staff members have specific roles and specialties.

**Attributes:**
- id (PK): Unique identifier
- first_name, last_name: Staff name
- email (UNIQUE): Contact email
- phone: Contact phone
- role: Job title (e.g., "Maintenance Supervisor", "Plumber")
- specialties (JSON): Array of expertise areas
- active: Employment status
- hire_date: Employment start date
- created_at, updated_at: Audit timestamps

**Purpose:** Represents maintenance personnel who are assigned to and complete requests.

---

### REQUEST Entity
Central entity representing maintenance requests submitted by tenants. Tracks the complete lifecycle from creation to resolution with assignment history and notes.

**Attributes:**
- id (PK): Unique identifier
- external_id (UNIQUE): Human-readable ID (e.g., "REQ-0186")
- tenant_id (FK): Requesting tenant
- unit_id (FK): Location of issue
- building_id (FK): Building context
- issue_type (ENUM): Category (Plumbing, Electrical, HVAC, etc.)
- priority (ENUM): Low, Medium, High, Emergency
- status (ENUM): OPEN, IN_PROGRESS, PENDING, COMPLETED, CLOSED
- description: Detailed issue description
- target_sla_hours: Expected resolution time
- location_details (JSON): Specific location information
- assignments (JSON): Assignment history with staff_id and timestamps
- notes (JSON): Communication thread between tenants and staff
- created_at, updated_at, closed_at: Lifecycle timestamps
- resolution_notes: Completion details

**Purpose:** Core business entity that links all other entities and tracks maintenance workflow.

---

## 2.3 Relationships

### BUILDING → UNIT (One-to-Many)
- One building contains many units
- Relationship: "contains" or "has"
- Foreign Key: unit.building_id → building.id
- Delete Rule: CASCADE (if building deleted, all units deleted)
- Rationale: Units cannot exist without a parent building

### UNIT → TENANT (One-to-Many)
- One unit can be occupied by many tenants (over time)
- Relationship: "houses" or "occupied by"
- Foreign Key: tenant.unit_id → unit.id
- Delete Rule: SET NULL (preserves tenant history if unit deleted)
- Rationale: Maintains historical records of tenant occupancy

### TENANT → REQUEST (One-to-Many)
- One tenant can create many maintenance requests
- Relationship: "creates" or "submits"
- Foreign Key: request.tenant_id → tenant.id
- Delete Rule: SET NULL (preserves request history)
- Rationale: Requests remain for audit purposes even if tenant moves out

### UNIT → REQUEST (One-to-Many)
- One unit can have many maintenance requests
- Relationship: "has issues"
- Foreign Key: request.unit_id → unit.id
- Delete Rule: SET NULL (preserves request history)
- Rationale: Maintains maintenance history per unit

### BUILDING → REQUEST (One-to-Many)
- One building can have many maintenance requests
- Relationship: "receives"
- Foreign Key: request.building_id → building.id
- Delete Rule: SET NULL (preserves request history)
- Rationale: Building-level maintenance analytics

### STAFF ← REQUEST (Referenced in JSON)
- Staff members are referenced in request.assignments JSON array
- Not a traditional FK relationship
- Each assignment includes: staff_id, assigned_at, accepted_at, completed_at, notes
- Rationale: Allows multiple staff assignments over time with full audit trail

---

## 2.4 Entity-Relationship Diagram

**[INSERT ER_Diagram.png HERE]**

*Figure 1: Entity-Relationship Diagram showing five entities (BUILDING, UNIT, TENANT, STAFF, REQUEST) and their relationships with cardinality labels (1:M)*

---

# 3. DATA CONSTRAINTS (15 pts)

## 3.1 Constraint Summary Table

| Table | Attribute | Constraint Type | Reason |
|-------|-----------|----------------|--------|
| **buildings** | id | PRIMARY KEY, VARCHAR, NOT NULL | Unique building identifier |
| buildings | name | VARCHAR(200), NOT NULL | Building name required |
| **units** | id | PRIMARY KEY, VARCHAR, NOT NULL | Unique unit identifier |
| units | building_id | FOREIGN KEY, NOT NULL, CASCADE | Ensures referential integrity; cascading delete |
| units | (building_id, unit_number) | UNIQUE | Prevents duplicate unit numbers per building |
| **tenants** | id | PRIMARY KEY, VARCHAR, NOT NULL | Unique tenant identifier |
| tenants | email | UNIQUE, NOT NULL | Prevents duplicate accounts |
| tenants | unit_id | FOREIGN KEY, SET NULL | Maintains history if unit deleted |
| **staff** | id | PRIMARY KEY, VARCHAR, NOT NULL | Unique staff identifier |
| staff | email | UNIQUE, NOT NULL | Prevents duplicate accounts |
| staff | active | BOOLEAN, DEFAULT TRUE | Soft delete support |
| **requests** | id | PRIMARY KEY, VARCHAR, NOT NULL | Unique request identifier |
| requests | external_id | UNIQUE, NOT NULL | Human-readable request ID |
| requests | issue_type | ENUM (10 values) | Data integrity - valid issue types only |
| requests | priority | ENUM (4 values) | Data integrity - valid priorities only |
| requests | status | ENUM (5 values) | Data integrity - valid statuses only |
| requests | tenant_id | FOREIGN KEY, SET NULL | Preserves request if tenant deleted |
| requests | unit_id | FOREIGN KEY, SET NULL | Preserves request if unit deleted |
| requests | building_id | FOREIGN KEY, SET NULL | Preserves request if building deleted |
| requests | target_sla_hours | INTEGER, NOT NULL | Required for SLA tracking |

## 3.2 Constraint Implementation Code

### ENUM Type Definitions

```sql
-- Created by Nerice Rodrigues
-- Defines valid issue types for maintenance classification

CREATE TYPE issuetype AS ENUM (
    'Plumbing',
    'Electrical', 
    'HVAC',
    'Appliance',
    'Structural',
    'Pest Control',
    'Cleaning',
    'Security',
    'Landscaping',
    'Other'
);

-- Defines priority levels with SLA implications
CREATE TYPE priority AS ENUM (
    'Low',           -- 72-hour SLA
    'Medium',        -- 48-hour SLA
    'High',          -- 24-hour SLA
    'Emergency'      -- 4-hour SLA
);

-- Defines request lifecycle statuses
CREATE TYPE requeststatus AS ENUM (
    'OPEN',          -- Newly created
    'IN_PROGRESS',   -- Assigned and being worked on
    'PENDING',       -- Waiting for parts/approval
    'COMPLETED',     -- Work finished
    'CLOSED'         -- Closed by tenant
);
```

### Building Table Creation

```sql
-- Created by Rachana H Dharani
-- Parent entity in the hierarchy

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

### Units Table with Foreign Key and Unique Constraint

```sql
-- Modified by Nerice Rodrigues
-- Demonstrates CASCADE delete and composite UNIQUE constraint

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
    UNIQUE (building_id, unit_number)
);

-- Rationale for CASCADE: If a building is demolished/removed,
-- all its units should be automatically removed.
-- The UNIQUE constraint ensures no duplicate unit numbers
-- within the same building (e.g., two "204" units in Building A).
```

### Tenants Table with SET NULL Foreign Key

```sql
-- Created by Rachana H Dharani
-- Demonstrates SET NULL for historical data preservation

CREATE TABLE tenants (
    id VARCHAR NOT NULL,
    unit_id VARCHAR,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    emergency_contact JSON,
    lease_start DATE,
    lease_end DATE,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
    PRIMARY KEY (id),
    FOREIGN KEY(unit_id) REFERENCES units (id) ON DELETE SET NULL,
    UNIQUE (email)
);

-- Rationale for SET NULL: If a unit is deleted, we still want to
-- maintain tenant records for historical purposes (past leases,
-- rental history, etc.). The unit_id becomes NULL but tenant
-- record remains.
```

### Requests Table with Multiple Foreign Keys

```sql
-- Created by Nerice Rodrigues & Rachana H Dharani
-- Complex entity with multiple FKs and JSON columns

CREATE TABLE requests (
    id VARCHAR NOT NULL,
    external_id VARCHAR(50) NOT NULL,
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
    FOREIGN KEY(building_id) REFERENCES buildings (id) ON DELETE SET NULL,
    UNIQUE (external_id)
);

-- Rationale: Requests are permanent audit records. Even if tenant
-- moves out or unit is deleted, we preserve the request history
-- by using SET NULL. The external_id (e.g., "REQ-0186") provides
-- a human-readable unique identifier.

-- JSON columns allow complex nested data:
-- - assignments: Array of {staff_id, assigned_at, completed_at, notes}
-- - notes: Array of {id, author_id, body, created_at}
-- - location_details: {neighborhood, latitude, longitude}
```

---

# 4. DATABASE CREATION & QUERIES (60 pts)

## 4.1 Database Setup (20 pts)

### Cloud Database Configuration

**Provider:** NEON PostgreSQL (Serverless)  
**Connection Details:**
- Host: ep-broad-resonance-ade3fcco-pooler.c-2.us-east-1.aws.neon.tech
- Database: neondb
- Port: 5432
- SSL Mode: require
- Connection Pooling: Enabled

**Technology Stack:**
- SQLAlchemy 2.0.44 (AsyncIO support)
- AsyncPG 0.30.0 (Pure Python PostgreSQL driver)
- Psycopg2-binary 2.9.11 (Backup driver)

### Database Initialization

**Initialization Script:** `backend/init_db.py`

```python
# Created by Nerice Rodrigues
"""
Initialize database tables using SQLAlchemy ORM
"""

import asyncio
from app.database import engine
from app.models.db_models import Base

async def init_db():
    """Create all tables defined in ORM models."""
    async with engine.begin() as conn:
        # Drop all tables (for clean slate)
        # await conn.run_sync(Base.metadata.drop_all)
        
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    
    print("✅ Database tables created successfully!")

if __name__ == "__main__":
    asyncio.run(init_db())
```

**Execution Output:**
```
Creating database tables...
INFO sqlalchemy.engine.Engine CREATE TYPE issuetype AS ENUM ('Plumbing', 'Electrical', ...)
INFO sqlalchemy.engine.Engine CREATE TYPE priority AS ENUM ('Low', 'Medium', 'High', 'Emergency')
INFO sqlalchemy.engine.Engine CREATE TYPE requeststatus AS ENUM ('OPEN', 'IN_PROGRESS', ...)
INFO sqlalchemy.engine.Engine CREATE TABLE buildings (...)
INFO sqlalchemy.engine.Engine CREATE TABLE staff (...)
INFO sqlalchemy.engine.Engine CREATE TABLE units (... FOREIGN KEY(building_id) REFERENCES buildings ...)
INFO sqlalchemy.engine.Engine CREATE TABLE tenants (... FOREIGN KEY(unit_id) REFERENCES units ...)
INFO sqlalchemy.engine.Engine CREATE TABLE requests (... FOREIGN KEY(tenant_id, unit_id, building_id) ...)
INFO sqlalchemy.engine.Engine COMMIT
✅ Database tables created successfully!
```

**[INSERT Figure_A10_Database_Seeding.png HERE - Terminal showing successful creation]**

### Data Loading

**Seeding Script:** `backend/seed_pg_data.py`

Data source inspired by Boston 311 service requests with realistic Boston neighborhoods.

**Execution:**
```bash
python seed_pg_data.py
```

**Output:**
```
🌱 Starting database seeding...
Creating 5 buildings...
✅ Created 5 buildings
Creating 200 units (40 per building, 5 floors, 8 units per floor)...
✅ Created 200 units
Creating 100 tenants with emergency contacts...
✅ Created 100 tenants
Creating 5 staff members with specialties...
✅ Created 5 staff members
Creating 200 maintenance requests with assignments and notes...
✅ Created 200 requests

🎉 Database seeding completed successfully!
   - 5 buildings in Boston neighborhoods (Back Bay, Beacon Hill, South End, North End, Fenway)
   - 200 units across all buildings
   - 100 tenants (50% occupancy rate)
   - 5 staff members (Supervisor, Plumber, Electrician, HVAC Tech, General Maintenance)
   - 200 maintenance requests with varied statuses, priorities, and assignments
```

**[INSERT Figure_A12_Backend_Connected.png HERE - Backend startup showing PostgreSQL connection]**

### Sample Data Statistics

```sql
SELECT 
    'buildings' as table_name, COUNT(*) as row_count FROM buildings
UNION ALL
SELECT 'units', COUNT(*) FROM units
UNION ALL
SELECT 'tenants', COUNT(*) FROM tenants
UNION ALL
SELECT 'staff', COUNT(*) FROM staff
UNION ALL
SELECT 'requests', COUNT(*) FROM requests;
```

**Results:**
```
table_name  | row_count
------------|----------
buildings   | 5
units       | 200
tenants     | 100
staff       | 5
requests    | 200
```

---

## 4.2 CRUD Operations (20 pts)

### CREATE - Insert New Maintenance Request

**Endpoint:** `POST /requests`  
**File:** `backend/app/routers/requests.py`

```python
# Created by Nerice Rodrigues

@router.post("/", response_model=RequestResponse, status_code=status.HTTP_201_CREATED)
async def create_request(
    request_data: RequestCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new maintenance request.
    
    - Generates unique ID and external ID (REQ-####)
    - Sets initial status to OPEN
    - Calculates target SLA based on priority
    - Emergency: 4 hours, High: 24 hours, Medium/Low: 48-72 hours
    """
    
    # Generate unique identifiers
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
        # Set SLA target based on priority
        target_sla_hours=4 if request_data.priority == Priority.EMERGENCY else
                         24 if request_data.priority == Priority.HIGH else
                         48 if request_data.priority == Priority.MEDIUM else 72,
        location_details=request_data.location_details,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    # Add to database
    db.add(new_request)
    await db.commit()
    await db.refresh(new_request)
    
    return new_request
```

**Sample API Request:**
```json
POST http://127.0.0.1:8000/requests
Content-Type: application/json

{
  "tenant_id": "11ad68a5-7f6f-4b62-9b03-9d59e3da28d2",
  "unit_id": "443beb47-358f-4d9a-b600-5bded21723f2",
  "building_id": "028915a2-b50e-4283-a1e3-9126ecf325ff",
  "issue_type": "Plumbing",
  "priority": "High",
  "description": "Kitchen sink is leaking badly, water pooling on floor"
}
```

**Response:**
```json
{
  "id": "a3f2c9d1-4e5f-6a7b-8c9d-0e1f2a3b4c5d",
  "external_id": "REQ-2847",
  "status": "OPEN",
  "priority": "High",
  "issue_type": "Plumbing",
  "target_sla_hours": 24,
  "created_at": "2025-11-10T14:30:00",
  ...
}
```

**[INSERT Figure_A7_Create_Request_Form.png HERE - Screenshot of create request form from frontend]**

---

### READ - Query Requests with Filtering

**Endpoint:** `GET /requests?status=OPEN&priority=High`  
**File:** `backend/app/routers/requests.py`

```python
# Modified by Rachana H Dharani

@router.get("/", response_model=List[RequestResponse])
async def get_requests(
    status_filter: Optional[str] = None,
    priority_filter: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    Get all maintenance requests with optional filtering.
    
    Supports filtering by:
    - status (OPEN, IN_PROGRESS, COMPLETED, CLOSED)
    - priority (Low, Medium, High, Emergency)
    
    Results ordered by created_at (newest first)
    """
    
    # Build query
    query = select(Request).order_by(Request.created_at.desc())
    
    # Apply filters if provided
    if status_filter:
        query = query.where(Request.status == status_filter)
    
    if priority_filter:
        query = query.where(Request.priority == priority_filter)
    
    # Pagination
    query = query.offset(skip).limit(limit)
    
    # Execute query
    result = await db.execute(query)
    requests = result.scalars().all()
    
    return requests
```

**Generated SQL:**
```sql
-- SQLAlchemy generates this query
SELECT 
    requests.id, requests.external_id, requests.tenant_id,
    requests.unit_id, requests.building_id, requests.issue_type,
    requests.priority, requests.status, requests.description,
    requests.target_sla_hours, requests.location_details,
    requests.assignments, requests.notes, requests.created_at,
    requests.updated_at, requests.closed_at, requests.resolution_notes
FROM requests
WHERE requests.status = 'OPEN' AND requests.priority = 'High'
ORDER BY requests.created_at DESC
LIMIT 100 OFFSET 0;
```

**Sample Output (5 records):**
```json
[
  {
    "id": "fa6fcc29-1c6f-4cf7-86a5-9103bcbd80af",
    "external_id": "REQ-0186",
    "status": "CLOSED",
    "priority": "Emergency",
    "issue_type": "Plumbing",
    "description": "Door lock stuck",
    "assignments": [
      {
        "staff_id": "1f03f583-9dcd-4c2c-93c7-0bc51524de09",
        "assigned_at": "2025-11-10T02:54:30",
        "completed_at": "2025-11-12T14:54:30",
        "notes": "Working on it"
      }
    ],
    "created_at": "2025-11-09T19:54:30"
  },
  ...
]
```

**[INSERT Figure_A8_Requests_List.png HERE - Requests table from frontend]**

---

### UPDATE - Change Request Status

**Endpoint:** `PATCH /requests/{request_id}/status`  
**File:** `backend/app/routers/requests.py`

```python
# Created by Nerice Rodrigues

@router.patch("/{request_id}/status", response_model=RequestResponse)
async def update_request_status(
    request_id: str,
    status_update: RequestStatusUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update the status of a maintenance request.
    
    Status transitions:
    - OPEN → IN_PROGRESS (when assigned)
    - IN_PROGRESS → COMPLETED (when work finished)
    - COMPLETED → CLOSED (when tenant confirms)
    
    Automatically sets closed_at timestamp when status is COMPLETED or CLOSED.
    """
    
    # Find request
    result = await db.execute(
        select(Request).where(Request.id == request_id)
    )
    request_obj = result.scalar_one_or_none()
    
    if not request_obj:
        raise HTTPException(status_code=404, detail="Request not found")
    
    # Update status
    request_obj.status = status_update.status
    request_obj.updated_at = datetime.utcnow()
    
    # Set closed_at if completing/closing
    if status_update.status in [RequestStatus.COMPLETED, RequestStatus.CLOSED]:
        request_obj.closed_at = datetime.utcnow()
        if status_update.resolution_notes:
            request_obj.resolution_notes = status_update.resolution_notes
    
    await db.commit()
    await db.refresh(request_obj)
    
    return request_obj
```

**Generated SQL:**
```sql
UPDATE requests 
SET 
    status = 'COMPLETED',
    updated_at = '2025-11-10 15:30:00',
    closed_at = '2025-11-10 15:30:00',
    resolution_notes = 'Leak fixed, replaced faulty pipe seal'
WHERE id = 'fa6fcc29-1c6f-4cf7-86a5-9103bcbd80af';
```

**Sample API Request:**
```json
PATCH http://127.0.0.1:8000/requests/fa6fcc29-1c6f-4cf7-86a5-9103bcbd80af/status

{
  "status": "COMPLETED",
  "resolution_notes": "Leak fixed, replaced faulty pipe seal"
}
```

**[INSERT Figure_A9_Request_Details.png HERE - Request details showing updated status]**

---

### DELETE - Soft Delete Staff Member

**Endpoint:** `DELETE /staff/{staff_id}`  
**File:** `backend/app/routers/staff.py`

```python
# Modified by Rachana H Dharani

@router.delete("/{staff_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_staff(
    staff_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Soft delete a staff member (set active = False).
    
    We use soft delete instead of hard delete to:
    1. Preserve assignment history in requests
    2. Maintain audit trail
    3. Allow potential re-activation
    
    Inactive staff don't appear in assignment dropdowns
    but their past assignments remain visible.
    """
    
    # Find staff member
    result = await db.execute(
        select(Staff).where(Staff.id == staff_id)
    )
    staff_member = result.scalar_one_or_none()
    
    if not staff_member:
        raise HTTPException(status_code=404, detail="Staff member not found")
    
    # Soft delete - set active to False
    staff_member.active = False
    staff_member.updated_at = datetime.utcnow()
    
    await db.commit()
    
    return None  # 204 No Content response
```

**Generated SQL:**
```sql
-- Soft delete preserves data
UPDATE staff 
SET 
    active = FALSE,
    updated_at = '2025-11-10 15:45:00'
WHERE id = '1f03f583-9dcd-4c2c-93c7-0bc51524de09';

-- To query only active staff:
SELECT * FROM staff WHERE active = TRUE;
```

**Rationale for Soft Delete:**
- Preserves historical assignment data in requests.assignments JSON
- Allows administrators to view past work completed by former staff
- Enables re-activation if staff member returns
- Maintains data integrity without orphaning references

---

## 4.3 Analytical Queries & Visualization (10 pts)

### Query 1: Request Status Distribution

**Endpoint:** `GET /metrics/requests-by-status`  
**Purpose:** Count requests grouped by status for pie chart visualization  
**File:** `backend/app/routers/metrics.py`

```python
# Created by Nerice Rodrigues

@router.get("/requests-by-status")
async def get_requests_by_status(db: AsyncSession = Depends(get_db)):
    """
    Get count of requests grouped by status.
    
    Returns data for pie chart showing distribution of:
    - OPEN requests (need assignment)
    - IN_PROGRESS requests (being worked on)
    - COMPLETED requests (work finished)
    - CLOSED requests (confirmed by tenant)
    """
    
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
SELECT 
    requests.status,
    COUNT(requests.id) AS count
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

**Visualization:** Pie chart in React dashboard using Recharts library

---

### Query 2: Average Resolution Time

**Endpoint:** `GET /metrics/overview`  
**Purpose:** Calculate average time to complete requests (in hours)  
**File:** `backend/app/routers/metrics.py`

```python
# Modified by Rachana H Dharani

@router.get("/overview")
async def get_metrics_overview(db: AsyncSession = Depends(get_db)):
    """
    Get overview metrics including average resolution time.
    
    Calculates:
    1. Active (open/in-progress) request count
    2. Completed request count
    3. Average resolution time in hours
    4. SLA breach count
    """
    
    # Average resolution time (only completed/closed requests)
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
        "average_resolution_hours": round(avg_hours, 2) if avg_hours else 0,
        ...
    }
```

**Generated SQL:**
```sql
-- Extract epoch converts timestamps to seconds, divide by 3600 for hours
SELECT 
    AVG(EXTRACT(epoch FROM requests.closed_at - requests.created_at) / 3600) AS avg_hours
FROM requests
WHERE requests.status IN ('CLOSED', 'COMPLETED')
  AND requests.closed_at IS NOT NULL;
```

**Sample Output:**
```json
{
  "average_resolution_hours": 47.35,
  "active_requests": 147,
  "completed_requests": 53,
  "sla_breaches": 8
}
```

**Visualization:** KPI card displaying "Avg Resolution Time: 47.35 hours"

---

### Query 3: Requests Over Time (Trend Analysis)

**Endpoint:** `GET /metrics/requests-over-time?days=30`  
**Purpose:** Show request creation trends for line chart  
**File:** `backend/app/routers/metrics.py`

```python
# Created by Nerice Rodrigues

@router.get("/requests-over-time")
async def get_requests_over_time(days: int = 30, db: AsyncSession = Depends(get_db)):
    """
    Get request creation trends over the last N days.
    
    Groups requests by date and counts daily totals.
    Used for line chart showing workload trends.
    """
    
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
SELECT 
    DATE(requests.created_at) AS date,
    COUNT(requests.id) AS count
FROM requests
WHERE requests.created_at >= '2025-10-10 00:00:00'
GROUP BY DATE(requests.created_at)
ORDER BY DATE(requests.created_at);
```

**Sample Output:**
```json
[
  {"date": "2025-10-10", "count": 5},
  {"date": "2025-10-11", "count": 8},
  {"date": "2025-10-12", "count": 12},
  ...
  {"date": "2025-11-09", "count": 7}
]
```

**Visualization:** Line chart showing 30-day trend

---

### Query 4: SLA Breach Detection

**Purpose:** Identify requests that exceeded their target SLA  
**File:** `backend/app/routers/metrics.py`

```python
# Modified by Rachana H Dharani

async def get_sla_breaches(db: AsyncSession):
    """
    Count requests that exceeded their SLA target.
    
    Compares actual resolution time against target_sla_hours.
    Only counts completed/closed requests.
    
    SLA Targets:
    - Emergency: 4 hours
    - High: 24 hours
    - Medium: 48 hours
    - Low: 72 hours
    """
    
    breach_query = select(
        func.count(Request.id)
    ).where(
        and_(
            Request.status.in_([RequestStatus.CLOSED, RequestStatus.COMPLETED]),
            Request.closed_at.isnot(None),
            # Compare actual hours vs target
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

**Sample Result:** `8 SLA breaches` (displayed in KPI card)

**[INSERT Figure_A4_Dashboard.png HERE - Dashboard showing all visualizations]**

---

## 4.4 Authorship & References (10 pts)

### Code Authorship

All code was collaboratively developed by the team with clear task division:

**Nerice Rodrigues:**
- Database schema design and ER diagram
- SQLAlchemy ORM model definitions (db_models.py)
- CRUD operations implementation (routers)
- Analytical queries for metrics (metrics.py)
- Database initialization script (init_db.py)

**Rachana H Dharani:**
- Frontend React component development
- Dashboard visualization with Recharts
- Form validation and user input handling
- Data seeding script (seed_pg_data.py)
- Testing and debugging across full stack

### Dataset Reference

**Boston 311 Service Requests**
- **Source:** City of Boston Open Data Portal
- **URL:** https://data.boston.gov/dataset/311-service-requests
- **License:** Public Domain / Open Data
- **Usage:** Inspired our maintenance request categories, priority levels, and SLA requirements. Real Boston neighborhoods used (Back Bay, Beacon Hill, South End, North End, Fenway).
- **Note:** Sample data generated based on typical patterns observed in real 311 data, not actual records.

### Technical References

1. **SQLAlchemy 2.0 Documentation - AsyncIO Support**
   - URL: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
   - Used for: AsyncEngine, AsyncSession, and async query patterns
   - Sections referenced: "Using asyncio with SQLAlchemy", "Async Session", "Running Async Queries"

2. **FastAPI Official Documentation**
   - URL: https://fastapi.tiangolo.com/
   - Used for: API router structure, dependency injection, Pydantic models
   - Sections referenced: "Path Operations", "Dependencies", "Response Models"

3. **PostgreSQL ENUM Types**
   - URL: https://www.postgresql.org/docs/current/datatype-enum.html
   - Used for: Creating custom enum types for issue_type, priority, status
   - Implementation: CREATE TYPE commands in database initialization

4. **NEON PostgreSQL Documentation**
   - URL: https://neon.tech/docs
   - Used for: Serverless PostgreSQL setup, connection pooling, SSL configuration
   - Features used: Connection pooling, automatic backups, serverless scaling

5. **Recharts Documentation**
   - URL: https://recharts.org/en-US/
   - Used for: Line charts, pie charts, and responsive design
   - Components used: LineChart, PieChart, ResponsiveContainer

### Query References

- **Time-based calculations:** PostgreSQL EXTRACT function documentation
- **JSON column handling:** PostgreSQL JSON functions documentation
- **Aggregation queries:** SQLAlchemy func documentation

---

# 5. CONTRIBUTION SUMMARY (5 pts)

| Name | Task | Contribution Details | Hours |
|------|------|---------------------|-------|
| **Nerice Rodrigues** | Database Schema Design | Designed ER diagram, defined 5 entities with relationships, created ENUM types, implemented foreign key constraints | 6 |
| Nerice Rodrigues | Backend Development | Wrote SQLAlchemy ORM models, implemented CRUD operations in 6 routers (buildings, units, tenants, staff, requests, metrics), created database initialization script | 10 |
| Nerice Rodrigues | Data Migration | Migrated project from MongoDB to PostgreSQL, rewrote database layer with AsyncPG, updated all schemas to remove ObjectId dependencies | 8 |
| **Rachana H Dharani** | Frontend Development | Built React dashboard with 5+ components, implemented Recharts visualizations, created responsive forms with validation | 9 |
| Rachana H Dharani | Data Management | Created comprehensive seeding script with 510 realistic records, tested all data relationships, verified constraint enforcement | 6 |
| Rachana H Dharani | Testing & Debugging | Tested all API endpoints, verified CRUD operations, debugged CORS and database connection issues, validated data integrity | 4 |
| **Both** | Integration & Documentation | Connected frontend to PostgreSQL backend, captured screenshots, wrote submission documentation, final testing | 6 |

**Total Team Hours:** 49 hours  
**Project Duration:** 2 weeks (including migration from MongoDB to PostgreSQL)

### Task Distribution Rationale

**Nerice focused on:**
- Database architecture and backend logic
- Complex SQL queries and aggregations
- System migration and infrastructure

**Rachana focused on:**
- User interface and user experience
- Data visualization and dashboards
- Data quality and testing

**Collaborative work:**
- API design and endpoint structure
- Schema refinement based on frontend needs
- Bug fixing and performance optimization

---

# 6. AI TOOL CITATION

### Acknowledgments

This project utilized AI-powered development tools to enhance productivity and code quality:

**GitHub Copilot (GPT-4 powered)**
- **Access Dates:** October 28 - November 10, 2025
- **Usage:** Code completion suggestions, boilerplate generation, async/await patterns
- **Specific Areas:**
  - SQLAlchemy model definitions
  - FastAPI router structure
  - React component scaffolding
  - TypeScript type definitions

**ChatGPT (GPT-4)**
- **Access Date:** November 10, 2025
- **Usage:** Technical consultation and problem-solving
- **Specific Areas:**
  - MongoDB to PostgreSQL migration strategy
  - Complex SQL query optimization (SLA breach detection, time-based aggregations)
  - JSON column handling in PostgreSQL
  - Recharts configuration for dashboard visualizations
  - Database constraint recommendations

**Visual Studio IntelliSense / IntelliCode**
- **Usage:** Code autocompletion, refactoring suggestions, type inference
- **Areas:** Python type hints, FastAPI parameter annotations, React prop types

### AI Usage Policy Compliance

All AI-generated code suggestions were:
1. **Reviewed and understood** by team members before implementation
2. **Modified and customized** to fit project-specific requirements
3. **Tested thoroughly** to ensure correctness and performance
4. **Documented with comments** explaining logic and design decisions

**Important Note:** AI tools were used as assistants, not replacements for understanding. The team takes full responsibility for all code in the final submission.

---

# 7. APPENDIX - SCREENSHOTS

## Figure A1: NEON PostgreSQL Console - Database Tables

**[INSERT Figure_A1_NEON_Tables_List.png HERE]**

*Caption: NEON PostgreSQL console showing 5 tables (buildings, units, tenants, staff, requests) in neondb database with row counts. Connected to ep-broad-resonance-ade3fcco-pooler.c-2.us-east-1.aws.neon.tech.*

---

## Figure A2: Buildings Table Data

**[INSERT Figure_A2_Buildings_Data.png HERE]**

*Caption: Sample data from buildings table showing 5 apartment buildings in Boston neighborhoods (Back Bay, Beacon Hill, South End, North End, Fenway) with complete address information.*

---

## Figure A3: Requests Table with JSON Columns

**[INSERT Figure_A3_Requests_Data.png HERE]**

*Caption: Sample maintenance requests showing complex JSON data in assignments and notes columns. Demonstrates storage of staff assignment history with timestamps and communication thread.*

---

## Figure A4: React Dashboard Overview

**[INSERT Figure_A4_Dashboard_Overview.png HERE]**

*Caption: Main dashboard displaying KPI cards (Active Requests: 147, Completed: 53, Avg Resolution: 47.35 hours, SLA Breaches: 8) with line chart showing 30-day request trends and pie charts for status/priority distribution.*

---

## Figure A5: Request Analytics Charts

**[INSERT Figure_A5_Analytics_Charts.png HERE]**

*Caption: Detailed view of analytical visualizations: (1) Line chart showing daily request volume over 30 days, (2) Pie chart showing status distribution (OPEN: 85, IN_PROGRESS: 62, CLOSED: 38, COMPLETED: 15), (3) Pie chart showing priority distribution.*

---

## Figure A6: Buildings List View

**[INSERT Figure_A6_Buildings_List.png HERE]**

*Caption: React frontend displaying list of all 5 buildings with neighborhood, address, city, and total unit count. Table shows proper data retrieval from PostgreSQL.*

---

## Figure A7: Create New Request Form

**[INSERT Figure_A7_Create_Request_Form.png HERE]**

*Caption: Request creation form showing dropdown selectors for tenant, unit, building, issue type (Plumbing, Electrical, etc.), priority (Low, Medium, High, Emergency), and description text area. Demonstrates frontend validation and user input.*

---

## Figure A8: Maintenance Requests List

**[INSERT Figure_A8_Requests_List.png HERE]**

*Caption: Table view of maintenance requests with columns: External ID (REQ-####), Status (color-coded badges), Priority, Issue Type, Tenant Name, Unit Number. Shows filtering and sorting capabilities.*

---

## Figure A9: Request Details View

**[INSERT Figure_A9_Request_Details.png HERE]**

*Caption: Detailed view of single request showing complete information: request details, tenant/unit/building associations, assignment history with staff member and timestamps, and notes thread with tenant comments.*

---

## Figure A10: Database Seeding Success

**[INSERT Figure_A10_Database_Seeding.png HERE]**

*Caption: Terminal output from seed_pg_data.py showing successful creation of 5 buildings, 200 units, 100 tenants, 5 staff members, and 200 maintenance requests with confirmation message "Database seeding completed successfully!"*

---

## Figure A11: API Response - GET /buildings

**[INSERT Figure_A11_API_Response_Buildings.png HERE]**

*Caption: Browser showing JSON response from GET /buildings endpoint. Demonstrates successful data retrieval from NEON PostgreSQL through FastAPI backend. Response includes all building fields with timestamps.*

---

## Figure A12: Backend Connected to PostgreSQL

**[INSERT Figure_A12_Backend_Connected.png HERE]**

*Caption: Terminal output from uvicorn showing successful application startup: SQLAlchemy connection to NEON PostgreSQL, table verification queries, and message "Connected to PostgreSQL: neondb" followed by "Application startup complete." Running on http://127.0.0.1:8000.*

---

## Figure A13: API Documentation (Swagger UI) [Optional]

**[INSERT Figure_A13_Swagger_UI.png HERE]**

*Caption: FastAPI auto-generated Swagger UI at /docs endpoint showing all available endpoints organized by routers: buildings, units, tenants, staff, requests, metrics. Demonstrates RESTful API structure.*

---

## Figure A14: VS Code Project Structure [Optional]

**[INSERT Figure_A14_Project_Structure.png HERE]**

*Caption: VS Code file explorer showing organized project structure: backend/ (app, models, routers, config, database), frontend/ (src, components, services), database initialization scripts, and documentation files.*

---

# END OF DOCUMENT

---

**Document Information:**
- **Filename:** Rodrigues_Dharani_Milestone2_12751.pdf
- **Pages:** 12-15 (depending on screenshot sizes)
- **File Size:** ~5-15 MB (depends on image compression)
- **Format:** PDF (exported from Word)

**Submission Checklist:**
- ☐ All sections present (1-7)
- ☐ ER diagram inserted
- ☐ Minimum 8-10 screenshots included
- ☐ All code snippets formatted properly
- ☐ Contribution table filled
- ☐ AI citation included
- ☐ Page numbers added
- ☐ Spell-checked
- ☐ Exported as PDF
- ☐ File size under 20 MB

**Ready to Submit!** ✅
