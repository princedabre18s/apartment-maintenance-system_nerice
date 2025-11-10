"""
Seed PostgreSQL database with sample data.
Creates 5 buildings, 200 units, 100 tenants, 5 staff, and 200 maintenance requests.
"""
import asyncio
import uuid
from datetime import datetime, timedelta
from random import choice, randint, uniform
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.models.db_models import Building, Unit, Tenant, Staff, Request
from app.models import RequestStatus, Priority, IssueType

# Sample data
BUILDING_NAMES = ["Riverside Apartments", "Sunset Tower", "Harbor View", "Parkside Residences", "Downtown Plaza"]
NEIGHBORHOODS = ["Back Bay", "Beacon Hill", "South End", "North End", "Fenway"]
FIRST_NAMES = ["John", "Jane", "Michael", "Sarah", "David", "Emily", "Chris", "Jessica", "Daniel", "Ashley"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
STAFF_ROLES = ["Maintenance Supervisor", "Plumber", "Electrician", "HVAC Technician", "General Maintenance"]
SPECIALTIES = [["Plumbing", "Heating"], ["Electrical", "Security"], ["HVAC", "Appliances"], ["Structural", "Painting"], ["Cleaning", "Pest Control"]]
DESCRIPTIONS = [
    "Water leak under sink",
    "No hot water in bathroom",
    "AC not cooling properly",
    "Electrical outlet not working",
    "Refrigerator making strange noise",
    "Toilet constantly running",
    "Broken window latch",
    "Door lock stuck",
    "Pest control needed",
    "Smoke detector beeping"
]


async def seed_data():
    """Seed the database with sample data."""
    print("🌱 Starting database seeding...")
    
    async with AsyncSessionLocal() as session:
        try:
            # 1. Create Buildings
            print("Creating 5 buildings...")
            buildings = []
            for i, name in enumerate(BUILDING_NAMES):
                building = Building(
                    id=str(uuid.uuid4()),
                    name=name,
                    address=f"{100 + i * 50} Main Street",
                    neighborhood=NEIGHBORHOODS[i],
                    city="Boston",
                    state="MA",
                    zip_code=f"0210{i}",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                buildings.append(building)
                session.add(building)
            
            await session.flush()
            print(f"✅ Created {len(buildings)} buildings")
            
            # 2. Create Units (40 per building = 200 total)
            print("Creating 200 units...")
            units = []
            for building in buildings:
                for floor in range(1, 6):  # 5 floors
                    for unit_num in range(1, 9):  # 8 units per floor
                        unit = Unit(
                            id=str(uuid.uuid4()),
                            building_id=building.id,
                            unit_number=f"{floor}{unit_num:02d}",
                            floor=floor,
                            bedrooms=choice([1, 2, 3]),
                            bathrooms=choice([1, 2]),
                            square_feet=randint(600, 1500),
                            created_at=datetime.utcnow(),
                            updated_at=datetime.utcnow()
                        )
                        units.append(unit)
                        session.add(unit)
            
            await session.flush()
            print(f"✅ Created {len(units)} units")
            
            # 3. Create Tenants (100 tenants, 2 per unit for some units)
            print("Creating 100 tenants...")
            tenants = []
            for i in range(100):
                unit = choice(units)
                tenant = Tenant(
                    id=str(uuid.uuid4()),
                    full_name=f"{choice(FIRST_NAMES)} {choice(LAST_NAMES)}",
                    email=f"tenant{i+1}@example.com",
                    phone=f"617-555-{randint(1000, 9999)}",
                    unit_id=unit.id,
                    move_in_date=datetime.utcnow() - timedelta(days=randint(30, 730)),
                    lease_end_date=datetime.utcnow() + timedelta(days=randint(30, 365)),
                    emergency_contact={
                        "name": f"{choice(FIRST_NAMES)} {choice(LAST_NAMES)}",
                        "phone": f"617-555-{randint(1000, 9999)}",
                        "relationship": choice(["Parent", "Sibling", "Friend", "Spouse"])
                    },
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                tenants.append(tenant)
                session.add(tenant)
            
            await session.flush()
            print(f"✅ Created {len(tenants)} tenants")
            
            # 4. Create Staff (5 staff members)
            print("Creating 5 staff members...")
            staff_members = []
            for i in range(5):
                staff = Staff(
                    id=str(uuid.uuid4()),
                    full_name=f"{choice(FIRST_NAMES)} {choice(LAST_NAMES)}",
                    email=f"staff{i+1}@maintenance.com",
                    phone=f"617-555-{randint(1000, 9999)}",
                    role=STAFF_ROLES[i],
                    specialties=SPECIALTIES[i],
                    hire_date=datetime.utcnow() - timedelta(days=randint(365, 1825)),
                    active=True,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                staff_members.append(staff)
                session.add(staff)
            
            await session.flush()
            print(f"✅ Created {len(staff_members)} staff members")
            
            # 5. Create Requests (200 requests)
            print("Creating 200 maintenance requests...")
            requests = []
            statuses = [RequestStatus.OPEN, RequestStatus.IN_PROGRESS, RequestStatus.COMPLETED, RequestStatus.CLOSED]
            priorities = [Priority.LOW, Priority.MEDIUM, Priority.HIGH, Priority.EMERGENCY]
            issue_types = list(IssueType)
            
            for i in range(200):
                tenant = choice(tenants)
                # Get the tenant's unit - use select() instead of query()
                unit_query = select(Unit).where(Unit.id == tenant.unit_id)
                unit_result = await session.execute(unit_query)
                unit = unit_result.scalar_one()
                
                status = choice(statuses)
                priority = choice(priorities)
                created_at = datetime.utcnow() - timedelta(days=randint(0, 90))
                
                # Create request
                request = Request(
                    id=str(uuid.uuid4()),
                    external_id=f"REQ-{i+1:04d}",
                    tenant_id=tenant.id,
                    unit_id=unit.id,
                    building_id=unit.building_id,
                    issue_type=choice(issue_types),
                    priority=priority,
                    description=choice(DESCRIPTIONS),
                    target_sla_hours=72 if priority == Priority.LOW else (48 if priority == Priority.MEDIUM else (24 if priority == Priority.HIGH else 4)),
                    status=status,
                    created_at=created_at,
                    updated_at=created_at + timedelta(hours=randint(1, 48)),
                    closed_at=created_at + timedelta(hours=randint(24, 168)) if status in [RequestStatus.COMPLETED, RequestStatus.CLOSED] else None,
                    assignments=[],
                    notes=[],
                    resolution_notes="Issue resolved successfully" if status in [RequestStatus.COMPLETED, RequestStatus.CLOSED] else None,
                    location_details={
                        "neighborhood": unit.unit_number,
                        "latitude": uniform(42.3, 42.4),
                        "longitude": uniform(-71.1, -71.0)
                    }
                )
                
                # Add assignments for in_progress/completed/closed requests
                if status in [RequestStatus.IN_PROGRESS, RequestStatus.COMPLETED, RequestStatus.CLOSED]:
                    assigned_staff = choice(staff_members)
                    assignment = {
                        "staff_id": assigned_staff.id,
                        "assigned_at": (created_at + timedelta(hours=randint(1, 12))).isoformat(),
                        "accepted_at": (created_at + timedelta(hours=randint(13, 24))).isoformat(),
                        "completed_at": (created_at + timedelta(hours=randint(25, 72))).isoformat() if status in [RequestStatus.COMPLETED, RequestStatus.CLOSED] else None,
                        "notes": "Working on it"
                    }
                    request.assignments = [assignment]
                
                # Add notes for some requests
                if randint(1, 3) == 1:  # 33% chance
                    note = {
                        "id": str(uuid.uuid4()),
                        "author_type": "tenant",
                        "author_id": tenant.id,
                        "author_name": tenant.full_name,
                        "body": "Please fix this as soon as possible.",
                        "created_at": (created_at + timedelta(hours=randint(1, 6))).isoformat()
                    }
                    request.notes = [note]
                
                requests.append(request)
                session.add(request)
            
            await session.flush()
            print(f"✅ Created {len(requests)} requests")
            
            # Commit all changes
            await session.commit()
            print("\n🎉 Database seeding completed successfully!")
            print(f"   - {len(buildings)} buildings")
            print(f"   - {len(units)} units")
            print(f"   - {len(tenants)} tenants")
            print(f"   - {len(staff_members)} staff members")
            print(f"   - {len(requests)} maintenance requests")
            
        except Exception as e:
            await session.rollback()
            print(f"\n❌ Error during seeding: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(seed_data())
