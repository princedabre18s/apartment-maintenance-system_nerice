from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
import uuid

from ..database import get_db
from ..models import Unit, UnitCreate, UnitUpdate
from ..models.db_models import Unit as DBUnit, Building as DBBuilding, Tenant as DBTenant

router = APIRouter(prefix="/units", tags=["units"])


@router.post("/", response_model=Unit, status_code=status.HTTP_201_CREATED)
async def create_unit(unit: UnitCreate, db: AsyncSession = Depends(get_db)):
    """Create a new unit."""
    # Validate building exists
    building_query = select(DBBuilding).where(DBBuilding.id == unit.building_id)
    building_result = await db.execute(building_query)
    building = building_result.scalar_one_or_none()
    
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    
    # Check for duplicate unit number in same building
    duplicate_query = select(DBUnit).where(
        and_(
            DBUnit.building_id == unit.building_id,
            DBUnit.unit_number == unit.unit_number
        )
    )
    duplicate_result = await db.execute(duplicate_query)
    if duplicate_result.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Unit number already exists in this building"
        )
    
    db_unit = DBUnit(
        id=str(uuid.uuid4()),
        **unit.model_dump(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    db.add(db_unit)
    await db.flush()
    await db.refresh(db_unit)
    
    return Unit.model_validate(db_unit)


@router.get("/", response_model=List[Unit])
async def get_units(building_id: Optional[str] = None, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """Get all units with optional building filter."""
    query = select(DBUnit).offset(skip).limit(limit)
    
    if building_id:
        query = query.where(DBUnit.building_id == building_id)
    
    result = await db.execute(query)
    units = result.scalars().all()
    
    return [Unit.model_validate(unit) for unit in units]


@router.get("/{unit_id}", response_model=Unit)
async def get_unit(unit_id: str, db: AsyncSession = Depends(get_db)):
    """Get a specific unit by ID."""
    query = select(DBUnit).where(DBUnit.id == unit_id)
    result = await db.execute(query)
    unit = result.scalar_one_or_none()
    
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    
    return Unit.model_validate(unit)


@router.put("/{unit_id}", response_model=Unit)
async def update_unit(unit_id: str, unit_update: UnitUpdate, db: AsyncSession = Depends(get_db)):
    """Update a unit."""
    query = select(DBUnit).where(DBUnit.id == unit_id)
    result = await db.execute(query)
    db_unit = result.scalar_one_or_none()
    
    if not db_unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    
    update_data = {k: v for k, v in unit_update.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    # Check for duplicate unit number if updating
    if "unit_number" in update_data or "building_id" in update_data:
        new_unit_number = update_data.get("unit_number", db_unit.unit_number)
        new_building_id = update_data.get("building_id", db_unit.building_id)
        
        duplicate_query = select(DBUnit).where(
            and_(
                DBUnit.id != unit_id,
                DBUnit.building_id == new_building_id,
                DBUnit.unit_number == new_unit_number
            )
        )
        duplicate_result = await db.execute(duplicate_query)
        if duplicate_result.scalar_one_or_none():
            raise HTTPException(
                status_code=400,
                detail="Unit number already exists in this building"
            )
    
    for key, value in update_data.items():
        setattr(db_unit, key, value)
    
    db_unit.updated_at = datetime.utcnow()
    
    await db.flush()
    await db.refresh(db_unit)
    
    return Unit.model_validate(db_unit)


@router.delete("/{unit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_unit(unit_id: str, db: AsyncSession = Depends(get_db)):
    """Delete a unit."""
    # Check if unit has tenants
    tenants_query = select(func.count()).select_from(DBTenant).where(DBTenant.unit_id == unit_id)
    tenants_result = await db.execute(tenants_query)
    tenants_count = tenants_result.scalar()
    
    if tenants_count > 0:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete unit with {tenants_count} associated tenants"
        )
    
    query = select(DBUnit).where(DBUnit.id == unit_id)
    result = await db.execute(query)
    db_unit = result.scalar_one_or_none()
    
    if not db_unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    
    await db.delete(db_unit)
    
    return None
