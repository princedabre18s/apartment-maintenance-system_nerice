"""
Data Seeding Script for Apartment Maintenance Request System

This script loads Boston 311 Service Requests data, cleans and normalizes it,
maps it to the MongoDB schema, and inserts it into the database.

Usage:
    python scripts/seed_data.py --csv data/boston_311_sample.csv --mongo $MONGO_URI

AI Tool Acknowledgment:
    Portions of this code were generated using GitHub Copilot (GPT-4) on November 7, 2025.
"""

import argparse
import asyncio
import pandas as pd
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import random


# Status mapping from 311 data to our schema
STATUS_MAPPING = {
    "Open": "OPEN",
    "Closed": "CLOSED",
    "In Progress": "IN_PROGRESS",
    "Pending": "PENDING"
}

# Issue type mapping
ISSUE_TYPE_MAPPING = {
    "Plumbing": "Plumbing",
    "Electrical": "Electrical",
    "Heat/Lack of Heat": "HVAC",
    "HVAC": "HVAC",
    "Heating": "HVAC",
    "Air Conditioning": "HVAC",
    "Appliance": "Appliances",
    "Appliance Repair": "Appliances",
    "Sanitation": "Cleaning",
    "Pest Control": "Pest Control",
    "Rodent Activity": "Pest Control",
    "Unsanitary Conditions": "Cleaning",
    "Maintenance": "Other",
    "Structural": "Structural",
    "Security": "Security"
}

PRIORITY_MAPPING = {
    "Emergency": "Emergency",
    "High": "High",
    "Medium": "Medium",
    "Normal": "Medium",
    "Low": "Low"
}


async def create_indexes(db):
    """Create indexes for optimal query performance."""
    print("Creating indexes...")
    
    # Buildings indexes
    await db.buildings.create_index("name")
    
    # Units indexes
    await db.units.create_index("building_id")
    await db.units.create_index([("building_id", 1), ("unit_number", 1)], unique=True)
    
    # Tenants indexes
    await db.tenants.create_index("email", unique=True)
    await db.tenants.create_index("unit_id")
    
    # Staff indexes
    await db.staff.create_index("email", unique=True)
    await db.staff.create_index("active")
    
    # Requests indexes
    await db.requests.create_index("status")
    await db.requests.create_index("created_at")
    await db.requests.create_index("issue_type")
    await db.requests.create_index("tenant_id")
    await db.requests.create_index("building_id")
    await db.requests.create_index([("status", 1), ("created_at", -1)])
    
    print("Indexes created successfully")


async def seed_buildings(db):
    """Create sample buildings in Boston neighborhoods."""
    print("Seeding buildings...")
    
    buildings = [
        {
            "name": "Sunset Apartments",
            "address": "123 Maple Ave",
            "neighborhood": "Back Bay",
            "city": "Boston",
            "state": "MA",
            "zip_code": "02116",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Harbor View Residences",
            "address": "456 Ocean Drive",
            "neighborhood": "South Boston",
            "city": "Boston",
            "state": "MA",
            "zip_code": "02127",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Beacon Hill Towers",
            "address": "789 Charles Street",
            "neighborhood": "Beacon Hill",
            "city": "Boston",
            "state": "MA",
            "zip_code": "02114",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Jamaica Plain Commons",
            "address": "321 Centre Street",
            "neighborhood": "Jamaica Plain",
            "city": "Boston",
            "state": "MA",
            "zip_code": "02130",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Dorchester Heights",
            "address": "654 Dorchester Ave",
            "neighborhood": "Dorchester",
            "city": "Boston",
            "state": "MA",
            "zip_code": "02125",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    
    result = await db.buildings.insert_many(buildings)
    print(f"Inserted {len(result.inserted_ids)} buildings")
    return result.inserted_ids


async def seed_units(db, building_ids):
    """Create units for each building."""
    print("Seeding units...")
    
    units = []
    floors = ["A", "B", "C", "D"]
    
    for building_id in building_ids:
        for floor_letter in floors:
            for unit_num in range(1, 11):  # 10 units per floor
                unit_number = f"{floor_letter}-{unit_num:02d}"
                units.append({
                    "building_id": str(building_id),
                    "unit_number": unit_number,
                    "floor": floors.index(floor_letter) + 1,
                    "bedrooms": random.choice([1, 2, 2, 3]),
                    "bathrooms": random.choice([1, 1, 2]),
                    "square_feet": random.randint(600, 1500),
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                })
    
    result = await db.units.insert_many(units)
    print(f"Inserted {len(result.inserted_ids)} units")
    return result.inserted_ids


async def seed_tenants(db, unit_ids):
    """Create sample tenants."""
    print("Seeding tenants...")
    
    first_names = ["John", "Jane", "Michael", "Sarah", "David", "Emily", "James", "Emma", "Robert", "Olivia"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
    
    tenants = []
    for i, unit_id in enumerate(unit_ids[:100]):  # Create 100 tenants
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        email = f"{first_name.lower()}.{last_name.lower()}{i}@example.com"
        
        tenants.append({
            "full_name": f"{first_name} {last_name}",
            "email": email,
            "phone": f"617-555-{random.randint(1000, 9999)}",
            "unit_id": str(unit_id),
            "move_in_date": datetime.utcnow() - timedelta(days=random.randint(30, 730)),
            "lease_end_date": datetime.utcnow() + timedelta(days=random.randint(90, 365)),
            "emergency_contact": {
                "name": f"{random.choice(first_names)} {random.choice(last_names)}",
                "phone": f"617-555-{random.randint(1000, 9999)}",
                "relationship": random.choice(["Spouse", "Parent", "Sibling", "Friend"])
            },
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
    
    result = await db.tenants.insert_many(tenants)
    print(f"Inserted {len(result.inserted_ids)} tenants")
    return result.inserted_ids


async def seed_staff(db):
    """Create sample staff members."""
    print("Seeding staff...")
    
    staff = [
        {
            "full_name": "Jane Smith",
            "email": "jane.smith@maintenance.com",
            "phone": "617-555-0100",
            "role": "Maintenance Engineer",
            "specialties": ["Plumbing", "Electrical", "HVAC"],
            "hire_date": datetime(2023, 1, 15),
            "active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "full_name": "Mike Johnson",
            "email": "mike.johnson@maintenance.com",
            "phone": "617-555-0101",
            "role": "Electrician",
            "specialties": ["Electrical", "Appliances"],
            "hire_date": datetime(2023, 3, 20),
            "active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "full_name": "Sarah Williams",
            "email": "sarah.williams@maintenance.com",
            "phone": "617-555-0102",
            "role": "Plumber",
            "specialties": ["Plumbing"],
            "hire_date": datetime(2022, 8, 10),
            "active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "full_name": "Tom Brown",
            "email": "tom.brown@maintenance.com",
            "phone": "617-555-0103",
            "role": "HVAC Technician",
            "specialties": ["HVAC", "Appliances"],
            "hire_date": datetime(2023, 6, 5),
            "active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "full_name": "Lisa Martinez",
            "email": "lisa.martinez@maintenance.com",
            "phone": "617-555-0104",
            "role": "General Maintenance",
            "specialties": ["Cleaning", "Structural", "Other"],
            "hire_date": datetime(2023, 9, 12),
            "active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    
    result = await db.staff.insert_many(staff)
    print(f"Inserted {len(result.inserted_ids)} staff members")
    return result.inserted_ids


async def seed_requests(db, tenant_ids, unit_ids, building_ids, staff_ids, csv_file=None):
    """Create maintenance requests from CSV or generate sample data."""
    print("Seeding requests...")
    
    requests = []
    issue_types = ["Plumbing", "Electrical", "HVAC", "Appliances", "Cleaning", "Pest Control", "Security", "Structural", "Other"]
    priorities = ["Low", "Medium", "High", "Emergency"]
    statuses = ["OPEN", "IN_PROGRESS", "PENDING", "COMPLETED", "CLOSED"]
    
    # Generate sample requests
    for i in range(200):  # Create 200 requests
        tenant_id = random.choice(tenant_ids)
        # Get tenant's unit
        tenant = await db.tenants.find_one({"_id": tenant_id})
        unit_id = tenant["unit_id"]
        
        # Get unit's building
        unit = await db.units.find_one({"_id": ObjectId(unit_id)})
        building_id = unit["building_id"]
        
        issue_type = random.choice(issue_types)
        priority = random.choice(priorities)
        status = random.choice(statuses)
        
        # Generate realistic descriptions
        descriptions = {
            "Plumbing": ["Leaking faucet in kitchen", "Toilet not flushing properly", "Sink drain clogged", "Water pressure low"],
            "Electrical": ["Light switch not working", "Outlet not functioning", "Circuit breaker tripping", "Flickering lights"],
            "HVAC": ["Heating not working", "AC not cooling", "Thermostat broken", "Strange noises from heater"],
            "Appliances": ["Refrigerator not cooling", "Dishwasher leaking", "Stove burner not igniting", "Washing machine not spinning"],
            "Cleaning": ["Mold in bathroom", "Carpet needs cleaning", "Windows dirty", "Common area needs attention"],
            "Pest Control": ["Mice spotted in unit", "Cockroaches in kitchen", "Bed bugs suspected", "Ant infestation"],
            "Security": ["Lock broken on front door", "Security light out", "Intercom not working", "Garage door malfunctioning"],
            "Structural": ["Ceiling crack", "Wall damage", "Floor boards loose", "Door frame damaged"],
            "Other": ["General maintenance needed", "Inspection requested", "Paint touch-up needed", "Misc repair"]
        }
        
        created_at = datetime.utcnow() - timedelta(days=random.randint(1, 90))
        closed_at = None
        if status in ["COMPLETED", "CLOSED"]:
            closed_at = created_at + timedelta(hours=random.randint(1, 168))
        
        # Create assignments for in-progress or completed requests
        assignments = []
        if status != "OPEN":
            staff_id = random.choice(staff_ids)
            assignment = {
                "staff_id": str(staff_id),
                "assigned_at": created_at + timedelta(hours=random.randint(1, 24)),
                "accepted_at": created_at + timedelta(hours=random.randint(2, 48)),
                "completed_at": closed_at if status in ["COMPLETED", "CLOSED"] else None,
                "notes": "Will handle this ASAP"
            }
            assignments.append(assignment)
        
        # Create notes
        notes = []
        if random.random() > 0.5:  # 50% chance of having notes
            note = {
                "_id": str(ObjectId()),
                "author_type": "tenant",
                "author_id": str(tenant_id),
                "author_name": tenant["full_name"],
                "body": "Please fix this soon, it's causing problems.",
                "created_at": created_at + timedelta(hours=random.randint(1, 12))
            }
            notes.append(note)
        
        request = {
            "external_id": f"311-REQ-2024-{10000 + i:05d}",
            "tenant_id": str(tenant_id),
            "unit_id": unit_id,
            "building_id": building_id,
            "issue_type": issue_type,
            "priority": priority,
            "description": random.choice(descriptions.get(issue_type, ["Maintenance required"])),
            "status": status,
            "created_at": created_at,
            "updated_at": closed_at if closed_at else created_at + timedelta(hours=random.randint(1, 24)),
            "closed_at": closed_at,
            "target_sla_hours": 24 if priority == "Emergency" else 48 if priority == "High" else 72 if priority == "Medium" else 168,
            "assignments": assignments,
            "notes": notes,
            "location_details": {
                "neighborhood": random.choice(["Back Bay", "South Boston", "Beacon Hill", "Jamaica Plain", "Dorchester"]),
                "latitude": 42.3505 + random.uniform(-0.05, 0.05),
                "longitude": -71.0815 + random.uniform(-0.05, 0.05)
            },
            "resolution_notes": "Issue resolved successfully" if status in ["COMPLETED", "CLOSED"] else None
        }
        
        requests.append(request)
    
    result = await db.requests.insert_many(requests)
    print(f"Inserted {len(result.inserted_ids)} requests")
    return result.inserted_ids


async def main(mongo_uri, csv_file=None):
    """Main seeding function."""
    print(f"Connecting to MongoDB: {mongo_uri}")
    client = AsyncIOMotorClient(mongo_uri)
    db = client.apartment_maintenance
    
    try:
        # Clear existing data (optional - comment out if you want to keep existing data)
        print("Clearing existing data...")
        await db.buildings.delete_many({})
        await db.units.delete_many({})
        await db.tenants.delete_many({})
        await db.staff.delete_many({})
        await db.requests.delete_many({})
        
        # Seed data
        building_ids = await seed_buildings(db)
        unit_ids = await seed_units(db, building_ids)
        tenant_ids = await seed_tenants(db, unit_ids)
        staff_ids = await seed_staff(db)
        request_ids = await seed_requests(db, tenant_ids, unit_ids, building_ids, staff_ids, csv_file)
        
        # Create indexes
        await create_indexes(db)
        
        print("\n✅ Data seeding completed successfully!")
        print(f"   - Buildings: {len(building_ids)}")
        print(f"   - Units: {len(unit_ids)}")
        print(f"   - Tenants: {len(tenant_ids)}")
        print(f"   - Staff: {len(staff_ids)}")
        print(f"   - Requests: {len(request_ids)}")
        
    finally:
        client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed data into MongoDB")
    parser.add_argument("--mongo", required=True, help="MongoDB connection URI")
    parser.add_argument("--csv", help="Optional: Path to Boston 311 CSV file")
    
    args = parser.parse_args()
    
    asyncio.run(main(args.mongo, args.csv))
