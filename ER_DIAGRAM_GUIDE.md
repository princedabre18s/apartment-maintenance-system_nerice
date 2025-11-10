# 🎨 ER DIAGRAM CREATION GUIDE
## Apartment Maintenance Request System

**Tools You Can Use:**
1. **Draw.io** (https://app.diagrams.net) - FREE, easy, recommended
2. **Lucidchart** (https://lucidchart.com) - FREE tier available
3. **dbdiagram.io** (https://dbdiagram.io) - Code-based, FREE
4. **Hand-drawn** - Scan or photo (must be neat!)

---

## 📊 YOUR DATABASE STRUCTURE

### **Entities (5 Total):**

1. **BUILDING**
2. **UNIT**
3. **TENANT**
4. **STAFF**
5. **REQUEST**

---

## 🔗 RELATIONSHIPS

```
BUILDING (1) ──────< (M) UNIT
                      │
                      │ (1)
                      │
                      └──────< (M) TENANT
                                │
                                │ (1)
                                │
                                └──────< (M) REQUEST

STAFF ──────< (referenced in) REQUEST (assignments JSON)
```

**Relationship Details:**
- BUILDING to UNIT: One-to-Many (1:M) - One building has many units
- UNIT to TENANT: One-to-Many (1:M) - One unit can have many tenants (over time)
- TENANT to REQUEST: One-to-Many (1:M) - One tenant can create many requests
- UNIT to REQUEST: One-to-Many (1:M) - One unit can have many requests
- BUILDING to REQUEST: One-to-Many (1:M) - One building can have many requests
- STAFF to REQUEST: Referenced in JSON (staff assigned to requests)

---

## 📋 ENTITY DETAILS

### 1️⃣ **BUILDING**
```
┌─────────────────────────┐
│       BUILDING          │
├─────────────────────────┤
│ PK  id (VARCHAR)        │
│     name                │
│     address             │
│     neighborhood        │
│     city                │
│     state               │
│     zip_code            │
│     created_at          │
│     updated_at          │
└─────────────────────────┘
```

---

### 2️⃣ **UNIT**
```
┌─────────────────────────┐
│         UNIT            │
├─────────────────────────┤
│ PK  id (VARCHAR)        │
│ FK  building_id         │────► BUILDING
│     unit_number         │
│     floor               │
│     bedrooms            │
│     bathrooms           │
│     sq_ft               │
│     monthly_rent        │
│     is_occupied         │
│     created_at          │
│     updated_at          │
└─────────────────────────┘
    UNIQUE: (building_id, unit_number)
```

---

### 3️⃣ **TENANT**
```
┌─────────────────────────┐
│        TENANT           │
├─────────────────────────┤
│ PK  id (VARCHAR)        │
│ FK  unit_id             │────► UNIT
│     first_name          │
│     last_name           │
│     email (UNIQUE)      │
│     phone               │
│     emergency_contact   │ (JSON)
│     lease_start         │
│     lease_end           │
│     active              │
│     created_at          │
│     updated_at          │
└─────────────────────────┘
```

---

### 4️⃣ **STAFF**
```
┌─────────────────────────┐
│         STAFF           │
├─────────────────────────┤
│ PK  id (VARCHAR)        │
│     first_name          │
│     last_name           │
│     email (UNIQUE)      │
│     phone               │
│     role                │
│     specialties         │ (JSON)
│     active              │
│     hire_date           │
│     created_at          │
│     updated_at          │
└─────────────────────────┘
```

---

### 5️⃣ **REQUEST**
```
┌─────────────────────────┐
│        REQUEST          │
├─────────────────────────┤
│ PK  id (VARCHAR)        │
│     external_id (UNIQUE)│
│ FK  tenant_id           │────► TENANT
│ FK  unit_id             │────► UNIT
│ FK  building_id         │────► BUILDING
│     issue_type (ENUM)   │
│     priority (ENUM)     │
│     status (ENUM)       │
│     description         │
│     target_sla_hours    │
│     location_details    │ (JSON)
│     assignments         │ (JSON - references STAFF)
│     notes               │ (JSON)
│     created_at          │
│     updated_at          │
│     closed_at           │
│     resolution_notes    │
└─────────────────────────┘
```

**ENUM Types:**
- **issue_type:** Plumbing, Electrical, HVAC, Appliance, Structural, Pest Control, Cleaning, Security, Landscaping, Other
- **priority:** Low, Medium, High, Emergency
- **status:** OPEN, IN_PROGRESS, PENDING, COMPLETED, CLOSED

---

## 🎨 DRAWING INSTRUCTIONS

### **Using Draw.io (Recommended):**

1. **Go to:** https://app.diagrams.net
2. **Choose:** "Create New Diagram"
3. **Select:** "Entity Relation" template
4. **Add Entities:**
   - Drag "Entity" shape for each table
   - Double-click to rename (BUILDING, UNIT, TENANT, STAFF, REQUEST)
   - Add attributes (drag "Attribute" shape)
   - Mark primary keys with underline or (PK)
   - Mark foreign keys with (FK)

5. **Add Relationships:**
   - Use "Relationship" connector
   - Label with "1" on one side, "M" on many side
   - Add relationship name (e.g., "has", "belongs to", "creates")

6. **Format:**
   - Use consistent colors (blue for entities, green for relationships)
   - Align boxes neatly
   - Use grid snap for cleaner look

7. **Export:**
   - File → Export As → PNG
   - Choose 300 DPI for high quality
   - Save as "ER_Diagram.png"

---

### **Using dbdiagram.io (Code-Based):**

1. **Go to:** https://dbdiagram.io
2. **Paste this code:**

```
Table buildings {
  id varchar [pk]
  name varchar(200)
  address varchar(500)
  neighborhood varchar(100)
  city varchar(100)
  state varchar(2)
  zip_code varchar(10)
  created_at timestamp
  updated_at timestamp
}

Table units {
  id varchar [pk]
  building_id varchar [ref: > buildings.id]
  unit_number varchar(20)
  floor integer
  bedrooms integer
  bathrooms decimal
  sq_ft integer
  monthly_rent decimal
  is_occupied boolean
  created_at timestamp
  updated_at timestamp
  
  indexes {
    (building_id, unit_number) [unique]
  }
}

Table tenants {
  id varchar [pk]
  unit_id varchar [ref: > units.id]
  first_name varchar(100)
  last_name varchar(100)
  email varchar(255) [unique]
  phone varchar(20)
  emergency_contact json
  lease_start date
  lease_end date
  active boolean
  created_at timestamp
  updated_at timestamp
}

Table staff {
  id varchar [pk]
  first_name varchar(100)
  last_name varchar(100)
  email varchar(255) [unique]
  phone varchar(20)
  role varchar(100)
  specialties json
  active boolean
  hire_date date
  created_at timestamp
  updated_at timestamp
}

Table requests {
  id varchar [pk]
  external_id varchar(50) [unique]
  tenant_id varchar [ref: > tenants.id]
  unit_id varchar [ref: > units.id]
  building_id varchar [ref: > buildings.id]
  issue_type varchar
  priority varchar
  status varchar
  description text
  target_sla_hours integer
  location_details json
  assignments json
  notes json
  created_at timestamp
  updated_at timestamp
  closed_at timestamp
  resolution_notes text
}
```

3. **Export:**
   - Click "Export" button
   - Choose PNG or PDF
   - Download

---

## ✅ WHAT YOUR DIAGRAM SHOULD SHOW

**Required Elements:**
- [ ] All 5 entities (BUILDING, UNIT, TENANT, STAFF, REQUEST)
- [ ] Primary keys marked (PK) or underlined
- [ ] Foreign keys marked (FK)
- [ ] Relationship lines connecting entities
- [ ] Cardinality labels (1, M) on both ends of relationships
- [ ] Clear and readable labels

**Nice to Have:**
- [ ] ENUM types noted for issue_type, priority, status
- [ ] JSON fields noted for assignments, notes, emergency_contact
- [ ] UNIQUE constraints shown
- [ ] Descriptive relationship names ("has", "belongs to", "creates")

---

## 🎨 COLOR SCHEME SUGGESTIONS

**For Professional Look:**
- **Entities:** Light blue background (#E3F2FD)
- **Primary Keys:** Bold or different color (#1976D2)
- **Foreign Keys:** Italic or different color (#F57C00)
- **Relationships:** Dark lines with arrow heads
- **JSON Fields:** Light green highlight (#C8E6C9)

---

## 📐 LAYOUT SUGGESTION

```
                    BUILDING
                        │
                        │ 1:M
                        ▼
                      UNIT
                        │
                        │ 1:M
                        ▼
                     TENANT
                        │
                        │ 1:M
                        ▼
    STAFF ─────────► REQUEST
      (referenced    (has FKs to
       in JSON)      tenant, unit,
                     building)
```

**Alternative Layout (More Compact):**
```
BUILDING ──1:M──► UNIT ──1:M──► TENANT
    │               │               │
    │               │               │
    └───────────────┴───────────────┴──► REQUEST ◄─── STAFF
                                                   (JSON ref)
```

---

## 🖨️ EXPORT SETTINGS

**For Word Document:**
- Format: PNG
- Resolution: 300 DPI minimum
- Size: Fit to page width (about 6-7 inches)
- Background: White (for printing)

**For PDF:**
- Format: PDF
- Page size: Letter (8.5 x 11)
- Margins: 0.5 inch
- Orientation: Landscape (if diagram is wide)

---

## ⏰ TIME ESTIMATE

- **Draw.io:** 15-20 minutes
- **dbdiagram.io:** 5-10 minutes (using provided code)
- **Hand-drawn:** 20-30 minutes (must be very neat!)

---

## 💡 QUICK TIP

**If you're short on time:**
1. Use dbdiagram.io with the code provided above
2. Copy-paste the entire code block
3. Let it auto-generate the diagram
4. Export as PNG
5. Done in 5 minutes! ✨

---

## 📸 FINAL STEP

After creating your ER diagram:
1. Export as high-resolution PNG
2. Save as "ER_Diagram.png"
3. Insert into your Word document in **Section 2: Conceptual Schema**
4. Add caption: "Figure 1: Entity-Relationship Diagram for Apartment Maintenance System"

---

**Your diagram should clearly show how buildings contain units, units house tenants, tenants create requests, and staff handle requests! 🎨**
