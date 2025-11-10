# MongoDB Schema Design - Apartment Maintenance Request System

## Collections Overview

This document describes the MongoDB database schema for the Apartment Maintenance Request System. The system uses document-based collections with ObjectId references for relationships.

---

## Collection: `buildings`

Stores information about apartment buildings in the system.

```json
{
  "_id": ObjectId("672d8b3e2b4f5c001a123456"),
  "name": "Sunset Apartments",
  "address": "123 Maple Ave",
  "neighborhood": "Back Bay",
  "city": "Boston",
  "state": "MA",
  "zip_code": "02116",
  "created_at": ISODate("2025-01-01T00:00:00Z"),
  "updated_at": ISODate("2025-01-01T00:00:00Z")
}
```

**Indexes:**
- `_id` (default)
- `name` (text index for search)

---

## Collection: `units`

Stores information about individual apartment units within buildings.

```json
{
  "_id": ObjectId("672d8b3e2b4f5c001a123457"),
  "building_id": ObjectId("672d8b3e2b4f5c001a123456"),
  "unit_number": "A-203",
  "floor": 2,
  "bedrooms": 2,
  "bathrooms": 1,
  "square_feet": 950,
  "created_at": ISODate("2025-01-01T00:00:00Z"),
  "updated_at": ISODate("2025-01-01T00:00:00Z")
}
```

**Indexes:**
- `_id` (default)
- `building_id` (for lookups)
- Compound index on `building_id` + `unit_number` (unique)

---

## Collection: `tenants`

Stores tenant information and their association with units.

```json
{
  "_id": ObjectId("672d8b3e2b4f5c001a123458"),
  "full_name": "John Doe",
  "email": "john.doe@example.com",
  "phone": "617-555-0123",
  "unit_id": ObjectId("672d8b3e2b4f5c001a123457"),
  "move_in_date": ISODate("2024-06-01T00:00:00Z"),
  "lease_end_date": ISODate("2025-06-01T00:00:00Z"),
  "emergency_contact": {
    "name": "Jane Doe",
    "phone": "617-555-0124",
    "relationship": "Spouse"
  },
  "created_at": ISODate("2025-01-01T00:00:00Z"),
  "updated_at": ISODate("2025-01-01T00:00:00Z")
}
```

**Indexes:**
- `_id` (default)
- `email` (unique)
- `unit_id` (for lookups)

---

## Collection: `staff`

Stores maintenance staff and administrator information.

```json
{
  "_id": ObjectId("672d8b3e2b4f5c001a123459"),
  "full_name": "Jane Smith",
  "email": "jane.smith@maintenance.com",
  "phone": "617-555-0125",
  "role": "Maintenance Engineer",
  "specialties": ["Plumbing", "Electrical", "HVAC"],
  "hire_date": ISODate("2023-01-15T00:00:00Z"),
  "active": true,
  "created_at": ISODate("2025-01-01T00:00:00Z"),
  "updated_at": ISODate("2025-01-01T00:00:00Z")
}
```

**Indexes:**
- `_id` (default)
- `email` (unique)
- `active` (for filtering)

---

## Collection: `requests`

The core collection storing all maintenance requests with embedded assignments and notes.

```json
{
  "_id": ObjectId("672d8b3e2b4f5c001a12345a"),
  "external_id": "311-REQ-2024-0091",
  "tenant_id": ObjectId("672d8b3e2b4f5c001a123458"),
  "unit_id": ObjectId("672d8b3e2b4f5c001a123457"),
  "building_id": ObjectId("672d8b3e2b4f5c001a123456"),
  "issue_type": "Plumbing",
  "priority": "Medium",
  "description": "Kitchen sink is leaking underneath. Water pools on cabinet floor.",
  "status": "OPEN",
  "created_at": ISODate("2025-11-06T08:00:00Z"),
  "updated_at": ISODate("2025-11-06T10:30:00Z"),
  "closed_at": null,
  "target_sla_hours": 72,
  "assignments": [
    {
      "staff_id": ObjectId("672d8b3e2b4f5c001a123459"),
      "assigned_at": ISODate("2025-11-06T09:00:00Z"),
      "accepted_at": ISODate("2025-11-06T09:15:00Z"),
      "completed_at": null,
      "notes": "Will inspect tomorrow morning"
    }
  ],
  "notes": [
    {
      "_id": ObjectId("672d8b3e2b4f5c001a12345b"),
      "author_type": "tenant",
      "author_id": ObjectId("672d8b3e2b4f5c001a123458"),
      "author_name": "John Doe",
      "body": "Water is still leaking. Getting worse.",
      "created_at": ISODate("2025-11-06T10:30:00Z")
    },
    {
      "_id": ObjectId("672d8b3e2b4f5c001a12345c"),
      "author_type": "staff",
      "author_id": ObjectId("672d8b3e2b4f5c001a123459"),
      "author_name": "Jane Smith",
      "body": "Parts ordered. Will fix by Friday.",
      "created_at": ISODate("2025-11-06T11:00:00Z")
    }
  ],
  "location_details": {
    "neighborhood": "Back Bay",
    "latitude": 42.3505,
    "longitude": -71.0815
  },
  "resolution_notes": null
}
```

**Field Descriptions:**

- `external_id`: Optional reference to external system (e.g., Boston 311)
- `status`: One of ["OPEN", "IN_PROGRESS", "PENDING", "COMPLETED", "CLOSED"]
- `priority`: One of ["Low", "Medium", "High", "Emergency"]
- `issue_type`: Categories like "Plumbing", "Electrical", "HVAC", "Appliances", "Cleaning", "Pest Control", "Security", "Other"
- `target_sla_hours`: Expected resolution time in hours (varies by priority)
- `assignments`: Array of staff assignments with timestamps
- `notes`: Embedded communication history between tenants and staff

**Indexes:**
- `_id` (default)
- `status` (for filtering)
- `created_at` (for sorting and time-based queries)
- `issue_type` (for analytics)
- `tenant_id` (for tenant dashboard)
- `building_id` (for building-level reports)
- Compound index on `status` + `created_at` (for performance)

---

## Data Constraints

### Field Validations

**Buildings:**
- `name`: Required, max 200 characters
- `address`: Required
- `neighborhood`: Optional

**Units:**
- `unit_number`: Required, unique per building
- `building_id`: Required, must reference valid building

**Tenants:**
- `full_name`: Required
- `email`: Required, valid email format, unique
- `phone`: Optional, valid phone format
- `unit_id`: Required, must reference valid unit

**Staff:**
- `full_name`: Required
- `email`: Required, valid email format, unique
- `role`: Required
- `active`: Boolean, default true

**Requests:**
- `tenant_id`: Required, must reference valid tenant
- `unit_id`: Required, must reference valid unit
- `issue_type`: Required, must be from predefined list
- `priority`: Required, must be from ["Low", "Medium", "High", "Emergency"]
- `status`: Required, must be from ["OPEN", "IN_PROGRESS", "PENDING", "COMPLETED", "CLOSED"]
- `description`: Required, max 2000 characters
- `target_sla_hours`: Required, positive integer

---

## Relationships

```
buildings (1) ──→ (M) units
units (1) ──→ (M) tenants
tenants (1) ──→ (M) requests
staff (1) ──→ (M) assignments (embedded in requests)
units (1) ──→ (M) requests
buildings (1) ──→ (M) requests
```

---

## Sample Aggregation Queries

### Average Resolution Time
```javascript
db.requests.aggregate([
  { $match: { status: "CLOSED", closed_at: { $ne: null } } },
  { $project: {
      resolution_time_hours: {
        $divide: [
          { $subtract: ["$closed_at", "$created_at"] },
          3600000
        ]
      }
    }
  },
  { $group: {
      _id: null,
      avg_resolution_hours: { $avg: "$resolution_time_hours" }
    }
  }
])
```

### Top Issue Types
```javascript
db.requests.aggregate([
  { $group: {
      _id: "$issue_type",
      count: { $sum: 1 }
    }
  },
  { $sort: { count: -1 } },
  { $limit: 5 }
])
```

### SLA Breach Count
```javascript
db.requests.aggregate([
  { $match: { status: "CLOSED" } },
  { $project: {
      resolution_time_hours: {
        $divide: [
          { $subtract: ["$closed_at", "$created_at"] },
          3600000
        ]
      },
      target_sla_hours: 1
    }
  },
  { $match: {
      $expr: { $gt: ["$resolution_time_hours", "$target_sla_hours"] }
    }
  },
  { $count: "sla_breaches" }
])
```

---

## Notes on Design

1. **Document Embedding vs. References**: Assignments and notes are embedded within requests for atomic updates and faster reads. Buildings, units, tenants, and staff use references due to their independent lifecycle and need for normalization.

2. **Timestamps**: All collections include `created_at` and `updated_at` for audit trails.

3. **Indexes**: Strategic indexes are placed on fields used in frequent queries (status, created_at, issue_type) and foreign key lookups.

4. **Scalability**: The schema supports multi-building organizations and can be extended with additional fields without breaking existing documents.

5. **Data Integrity**: Application-level validation ensures referential integrity since MongoDB doesn't enforce foreign key constraints.

---

**Schema Version**: 1.0  
**Last Updated**: November 7, 2025  
**Author**: Nerodr & Rdharani
