from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import uuid

from ..database import get_db
from ..models import Building, BuildingCreate, BuildingUpdate
from ..models.db_models import Building as DBBuilding, Unit as DBUnit

router = APIRouter(prefix="/buildings", tags=["buildings"])


@router.post("/", response_model=Building, status_code=status.HTTP_201_CREATED)
async def create_building(building: BuildingCreate, db: AsyncSession = Depends(get_db)):
    """Create a new building."""
    db_building = DBBuilding(
        id=str(uuid.uuid4()),
        **building.model_dump(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    db.add(db_building)
    await db.flush()
    await db.refresh(db_building)
    
    return Building.model_validate(db_building)


@router.get("/", response_model=List[Building])
async def get_buildings(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """Get all buildings with pagination."""
    query = select(DBBuilding).offset(skip).limit(limit)
    result = await db.execute(query)
    buildings = result.scalars().all()
    
    return [Building.model_validate(building) for building in buildings]


@router.get("/{building_id}", response_model=Building)
async def get_building(building_id: str, db: AsyncSession = Depends(get_db)):
    """Get a specific building by ID."""
    query = select(DBBuilding).where(DBBuilding.id == building_id)
    result = await db.execute(query)
    building = result.scalar_one_or_none()
    
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    
    return Building.model_validate(building)


@router.put("/{building_id}", response_model=Building)
async def update_building(building_id: str, building_update: BuildingUpdate, db: AsyncSession = Depends(get_db)):
    """Update a building."""
    # Check if building exists
    query = select(DBBuilding).where(DBBuilding.id == building_id)
    result = await db.execute(query)
    db_building = result.scalar_one_or_none()
    
    if not db_building:
        raise HTTPException(status_code=404, detail="Building not found")
    
    # Update only provided fields
    update_data = {k: v for k, v in building_update.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    for key, value in update_data.items():
        setattr(db_building, key, value)
    
    db_building.updated_at = datetime.utcnow()
    
    await db.flush()
    await db.refresh(db_building)
    
    return Building.model_validate(db_building)


@router.delete("/{building_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_building(building_id: str, db: AsyncSession = Depends(get_db)):
    """Delete a building."""
    # Check if building has associated units
    units_query = select(func.count()).select_from(DBUnit).where(DBUnit.building_id == building_id)
    units_result = await db.execute(units_query)
    units_count = units_result.scalar()
    
    if units_count > 0:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete building with {units_count} associated units"
        )
    
    # Get and delete building
    query = select(DBBuilding).where(DBBuilding.id == building_id)
    result = await db.execute(query)
    db_building = result.scalar_one_or_none()
    
    if not db_building:
        raise HTTPException(status_code=404, detail="Building not found")
    
    await db.delete(db_building)
    
    return None
