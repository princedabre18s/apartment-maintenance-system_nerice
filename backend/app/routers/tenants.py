from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
import uuid

from ..database import get_db
from ..models import Tenant, TenantCreate, TenantUpdate
from ..models.db_models import Tenant as DBTenant, Unit as DBUnit, Request as DBRequest

router = APIRouter(prefix="/tenants", tags=["tenants"])


@router.post("/", response_model=Tenant, status_code=status.HTTP_201_CREATED)
async def create_tenant(tenant: TenantCreate, db: AsyncSession = Depends(get_db)):
    """Create a new tenant."""
    # Validate unit exists
    unit_query = select(DBUnit).where(DBUnit.id == tenant.unit_id)
    unit_result = await db.execute(unit_query)
    unit = unit_result.scalar_one_or_none()
    
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    
    # Check for duplicate email
    email_query = select(DBTenant).where(DBTenant.email == tenant.email)
    email_result = await db.execute(email_query)
    if email_result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_tenant = DBTenant(
        id=str(uuid.uuid4()),
        **tenant.model_dump(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    db.add(db_tenant)
    await db.flush()
    await db.refresh(db_tenant)
    
    return Tenant.model_validate(db_tenant)


@router.get("/", response_model=List[Tenant])
async def get_tenants(unit_id: Optional[str] = None, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """Get all tenants with optional unit filter."""
    query = select(DBTenant).offset(skip).limit(limit)
    
    if unit_id:
        query = query.where(DBTenant.unit_id == unit_id)
    
    result = await db.execute(query)
    tenants = result.scalars().all()
    
    return [Tenant.model_validate(tenant) for tenant in tenants]


@router.get("/{tenant_id}", response_model=Tenant)
async def get_tenant(tenant_id: str, db: AsyncSession = Depends(get_db)):
    """Get a specific tenant by ID."""
    query = select(DBTenant).where(DBTenant.id == tenant_id)
    result = await db.execute(query)
    tenant = result.scalar_one_or_none()
    
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    return Tenant.model_validate(tenant)


@router.put("/{tenant_id}", response_model=Tenant)
async def update_tenant(tenant_id: str, tenant_update: TenantUpdate, db: AsyncSession = Depends(get_db)):
    """Update a tenant."""
    query = select(DBTenant).where(DBTenant.id == tenant_id)
    result = await db.execute(query)
    db_tenant = result.scalar_one_or_none()
    
    if not db_tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    update_data = {k: v for k, v in tenant_update.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    # Check for duplicate email if updating
    if "email" in update_data:
        duplicate_query = select(DBTenant).where(
            and_(
                DBTenant.id != tenant_id,
                DBTenant.email == update_data["email"]
            )
        )
        duplicate_result = await db.execute(duplicate_query)
        if duplicate_result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email already registered")
    
    for key, value in update_data.items():
        setattr(db_tenant, key, value)
    
    db_tenant.updated_at = datetime.utcnow()
    
    await db.flush()
    await db.refresh(db_tenant)
    
    return Tenant.model_validate(db_tenant)


@router.delete("/{tenant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tenant(tenant_id: str, db: AsyncSession = Depends(get_db)):
    """Delete a tenant."""
    # Check if tenant has requests
    requests_query = select(func.count()).select_from(DBRequest).where(DBRequest.tenant_id == tenant_id)
    requests_result = await db.execute(requests_query)
    requests_count = requests_result.scalar()
    
    if requests_count > 0:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete tenant with {requests_count} associated requests"
        )
    
    query = select(DBTenant).where(DBTenant.id == tenant_id)
    result = await db.execute(query)
    db_tenant = result.scalar_one_or_none()
    
    if not db_tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    await db.delete(db_tenant)
    
    return None
