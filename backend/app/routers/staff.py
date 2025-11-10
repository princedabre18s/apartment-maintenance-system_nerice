from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
import uuid

from ..database import get_db
from ..models import Staff, StaffCreate, StaffUpdate
from ..models.db_models import Staff as DBStaff

router = APIRouter(prefix="/staff", tags=["staff"])


@router.post("/", response_model=Staff, status_code=status.HTTP_201_CREATED)
async def create_staff(staff: StaffCreate, db: AsyncSession = Depends(get_db)):
    """Create a new staff member."""
    # Check for duplicate email
    email_query = select(DBStaff).where(DBStaff.email == staff.email)
    email_result = await db.execute(email_query)
    if email_result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_staff = DBStaff(
        id=str(uuid.uuid4()),
        **staff.model_dump(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    db.add(db_staff)
    await db.flush()
    await db.refresh(db_staff)
    
    return Staff.model_validate(db_staff)


@router.get("/", response_model=List[Staff])
async def get_staff(active: Optional[bool] = None, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """Get all staff members with optional active filter."""
    query = select(DBStaff).offset(skip).limit(limit)
    
    if active is not None:
        query = query.where(DBStaff.active == active)
    
    result = await db.execute(query)
    staff_list = result.scalars().all()
    
    return [Staff.model_validate(staff) for staff in staff_list]


@router.get("/{staff_id}", response_model=Staff)
async def get_staff_member(staff_id: str, db: AsyncSession = Depends(get_db)):
    """Get a specific staff member by ID."""
    query = select(DBStaff).where(DBStaff.id == staff_id)
    result = await db.execute(query)
    staff = result.scalar_one_or_none()
    
    if not staff:
        raise HTTPException(status_code=404, detail="Staff member not found")
    
    return Staff.model_validate(staff)


@router.put("/{staff_id}", response_model=Staff)
async def update_staff(staff_id: str, staff_update: StaffUpdate, db: AsyncSession = Depends(get_db)):
    """Update a staff member."""
    query = select(DBStaff).where(DBStaff.id == staff_id)
    result = await db.execute(query)
    db_staff = result.scalar_one_or_none()
    
    if not db_staff:
        raise HTTPException(status_code=404, detail="Staff member not found")
    
    update_data = {k: v for k, v in staff_update.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    # Check for duplicate email if updating
    if "email" in update_data:
        duplicate_query = select(DBStaff).where(
            and_(
                DBStaff.id != staff_id,
                DBStaff.email == update_data["email"]
            )
        )
        duplicate_result = await db.execute(duplicate_query)
        if duplicate_result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email already registered")
    
    for key, value in update_data.items():
        setattr(db_staff, key, value)
    
    db_staff.updated_at = datetime.utcnow()
    
    await db.flush()
    await db.refresh(db_staff)
    
    return Staff.model_validate(db_staff)


@router.delete("/{staff_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_staff(staff_id: str, db: AsyncSession = Depends(get_db)):
    """Delete a staff member (soft delete by setting active=False is recommended)."""
    query = select(DBStaff).where(DBStaff.id == staff_id)
    result = await db.execute(query)
    db_staff = result.scalar_one_or_none()
    
    if not db_staff:
        raise HTTPException(status_code=404, detail="Staff member not found")
    
    # Soft delete instead of hard delete
    db_staff.active = False
    db_staff.updated_at = datetime.utcnow()
    
    await db.flush()
    
    return None
