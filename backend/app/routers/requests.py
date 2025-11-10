from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
import uuid

from ..database import get_db
from ..models import (
    Request, RequestCreate, RequestUpdate, RequestStatus,
    AssignmentCreate, Assignment, NoteCreate, Note
)
from ..models.db_models import (
    Request as DBRequest, Tenant as DBTenant, Unit as DBUnit,
    Building as DBBuilding, Staff as DBStaff
)

router = APIRouter(prefix="/requests", tags=["requests"])


@router.post("/", response_model=Request, status_code=status.HTTP_201_CREATED)
async def create_request(request: RequestCreate, db: AsyncSession = Depends(get_db)):
    """Create a new maintenance request."""
    # Validate tenant exists
    tenant_query = select(DBTenant).where(DBTenant.id == request.tenant_id)
    tenant_result = await db.execute(tenant_query)
    if not tenant_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    # Validate unit exists
    unit_query = select(DBUnit).where(DBUnit.id == request.unit_id)
    unit_result = await db.execute(unit_query)
    if not unit_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Unit not found")
    
    # Validate building exists
    building_query = select(DBBuilding).where(DBBuilding.id == request.building_id)
    building_result = await db.execute(building_query)
    if not building_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Building not found")
    
    db_request = DBRequest(
        id=str(uuid.uuid4()),
        **request.model_dump(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        closed_at=None,
        assignments=[],
        notes=[],
        resolution_notes=None
    )
    
    db.add(db_request)
    await db.flush()
    await db.refresh(db_request)
    
    return Request.model_validate(db_request)


@router.get("/", response_model=List[Request])
async def get_requests(
    status_filter: Optional[RequestStatus] = Query(None, alias="status"),
    tenant_id: Optional[str] = None,
    building_id: Optional[str] = None,
    issue_type: Optional[str] = None,
    priority: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get all requests with optional filters."""
    query = select(DBRequest).offset(skip).limit(limit).order_by(desc(DBRequest.created_at))
    
    if status_filter:
        query = query.where(DBRequest.status == status_filter)
    if tenant_id:
        query = query.where(DBRequest.tenant_id == tenant_id)
    if building_id:
        query = query.where(DBRequest.building_id == building_id)
    if issue_type:
        query = query.where(DBRequest.issue_type == issue_type)
    if priority:
        query = query.where(DBRequest.priority == priority)
    
    result = await db.execute(query)
    requests = result.scalars().all()
    
    return [Request.model_validate(req) for req in requests]


@router.get("/{request_id}", response_model=Request)
async def get_request(request_id: str, db: AsyncSession = Depends(get_db)):
    """Get a specific request by ID."""
    query = select(DBRequest).where(DBRequest.id == request_id)
    result = await db.execute(query)
    request = result.scalar_one_or_none()
    
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    return Request.model_validate(request)


@router.put("/{request_id}", response_model=Request)
async def update_request(request_id: str, request_update: RequestUpdate, db: AsyncSession = Depends(get_db)):
    """Update a request."""
    query = select(DBRequest).where(DBRequest.id == request_id)
    result = await db.execute(query)
    db_request = result.scalar_one_or_none()
    
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    update_data = {k: v for k, v in request_update.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    # Handle status change to CLOSED
    if "status" in update_data and update_data["status"] in [RequestStatus.CLOSED, RequestStatus.COMPLETED]:
        if not db_request.closed_at:
            db_request.closed_at = datetime.utcnow()
    
    for key, value in update_data.items():
        setattr(db_request, key, value)
    
    db_request.updated_at = datetime.utcnow()
    
    await db.flush()
    await db.refresh(db_request)
    
    return Request.model_validate(db_request)


@router.delete("/{request_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_request(request_id: str, db: AsyncSession = Depends(get_db)):
    """Delete a request."""
    query = select(DBRequest).where(DBRequest.id == request_id)
    result = await db.execute(query)
    db_request = result.scalar_one_or_none()
    
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    await db.delete(db_request)
    
    return None


@router.post("/{request_id}/assign", response_model=Request)
async def assign_request(request_id: str, assignment: AssignmentCreate, db: AsyncSession = Depends(get_db)):
    """Assign a staff member to a request."""
    # Validate request exists
    request_query = select(DBRequest).where(DBRequest.id == request_id)
    request_result = await db.execute(request_query)
    db_request = request_result.scalar_one_or_none()
    
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    # Validate staff exists
    staff_query = select(DBStaff).where(DBStaff.id == assignment.staff_id)
    staff_result = await db.execute(staff_query)
    if not staff_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Staff member not found")
    
    # Check if already assigned
    for existing_assignment in db_request.assignments or []:
        if existing_assignment.get("staff_id") == assignment.staff_id and not existing_assignment.get("completed_at"):
            raise HTTPException(status_code=400, detail="Staff member already assigned to this request")
    
    # Create assignment
    new_assignment = {
        "staff_id": assignment.staff_id,
        "assigned_at": datetime.utcnow().isoformat(),
        "accepted_at": None,
        "completed_at": None,
        "notes": assignment.notes
    }
    
    # Update request
    current_assignments = db_request.assignments or []
    current_assignments.append(new_assignment)
    db_request.assignments = current_assignments
    db_request.status = RequestStatus.IN_PROGRESS
    db_request.updated_at = datetime.utcnow()
    
    await db.flush()
    await db.refresh(db_request)
    
    return Request.model_validate(db_request)


@router.post("/{request_id}/notes", response_model=Request)
async def add_note(request_id: str, note: NoteCreate, db: AsyncSession = Depends(get_db)):
    """Add a note to a request."""
    # Validate request exists
    query = select(DBRequest).where(DBRequest.id == request_id)
    result = await db.execute(query)
    db_request = result.scalar_one_or_none()
    
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    # Create note
    new_note = {
        "id": str(uuid.uuid4()),
        "author_type": note.author_type,
        "author_id": note.author_id,
        "author_name": note.author_name,
        "body": note.body,
        "created_at": datetime.utcnow().isoformat()
    }
    
    # Update request
    current_notes = db_request.notes or []
    current_notes.append(new_note)
    db_request.notes = current_notes
    db_request.updated_at = datetime.utcnow()
    
    await db.flush()
    await db.refresh(db_request)
    
    return Request.model_validate(db_request)


@router.post("/{request_id}/complete", response_model=Request)
async def complete_assignment(request_id: str, staff_id: str, db: AsyncSession = Depends(get_db)):
    """Mark an assignment as completed."""
    # Validate request exists
    query = select(DBRequest).where(DBRequest.id == request_id)
    result = await db.execute(query)
    db_request = result.scalar_one_or_none()
    
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    # Find and update the assignment
    assignments = db_request.assignments or []
    assignment_found = False
    
    for assignment in assignments:
        if assignment.get("staff_id") == staff_id and not assignment.get("completed_at"):
            assignment["completed_at"] = datetime.utcnow().isoformat()
            assignment_found = True
            break
    
    if not assignment_found:
        raise HTTPException(status_code=404, detail="Active assignment not found for this staff member")
    
    # Update request
    db_request.assignments = assignments
    db_request.status = RequestStatus.COMPLETED
    db_request.updated_at = datetime.utcnow()
    
    await db.flush()
    await db.refresh(db_request)
    
    return Request.model_validate(db_request)

