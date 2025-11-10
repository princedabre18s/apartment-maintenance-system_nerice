from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List, Any
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case, and_, cast, extract, Integer
from sqlalchemy.sql import text

from ..database import get_db
from ..models import RequestStatus
from ..models.db_models import Request as DBRequest, Building as DBBuilding, Staff as DBStaff

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("/overview")
async def get_metrics_overview(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    """
    Get comprehensive metrics overview for dashboard.
    Returns:
    - total_open_requests: Count of open requests
    - total_closed_requests: Count of closed requests
    - average_resolution_time: Average hours to close a request
    - top_issue_types: Top 5 issue types with counts
    - sla_breach_count: Number of requests that exceeded SLA
    - completion_rate: Percentage of closed requests
    """
    # Total open requests
    open_query = select(func.count()).select_from(DBRequest).where(
        DBRequest.status.in_([RequestStatus.OPEN, RequestStatus.IN_PROGRESS, RequestStatus.PENDING])
    )
    open_result = await db.execute(open_query)
    total_open = open_result.scalar()
    
    # Total closed requests
    closed_query = select(func.count()).select_from(DBRequest).where(
        DBRequest.status.in_([RequestStatus.CLOSED, RequestStatus.COMPLETED])
    )
    closed_result = await db.execute(closed_query)
    total_closed = closed_result.scalar()
    
    # Average resolution time
    avg_query = select(
        func.avg(
            func.extract('epoch', DBRequest.closed_at - DBRequest.created_at) / 3600
        ).label('avg_hours')
    ).where(
        and_(
            DBRequest.status.in_([RequestStatus.CLOSED, RequestStatus.COMPLETED]),
            DBRequest.closed_at.is_not(None)
        )
    )
    avg_result = await db.execute(avg_query)
    avg_hours = avg_result.scalar()
    average_resolution_time = round(float(avg_hours), 2) if avg_hours else 0
    
    # Top 5 issue types
    top_issues_query = select(
        DBRequest.issue_type.label('issue_type'),
        func.count().label('count')
    ).group_by(DBRequest.issue_type).order_by(func.count().desc()).limit(5)
    
    top_issues_result = await db.execute(top_issues_query)
    top_issue_types = [
        {"issue_type": str(row.issue_type), "count": row.count}
        for row in top_issues_result.fetchall()
    ]
    
    # SLA breach count
    sla_breach_query = select(func.count()).select_from(DBRequest).where(
        and_(
            DBRequest.status.in_([RequestStatus.CLOSED, RequestStatus.COMPLETED]),
            DBRequest.closed_at.is_not(None),
            func.extract('epoch', DBRequest.closed_at - DBRequest.created_at) / 3600 > DBRequest.target_sla_hours
        )
    )
    sla_breach_result = await db.execute(sla_breach_query)
    sla_breach_count = sla_breach_result.scalar()
    
    # Completion rate
    total_requests = total_open + total_closed
    completion_rate = round((total_closed / total_requests * 100), 2) if total_requests > 0 else 0
    
    return {
        "total_open_requests": total_open,
        "total_closed_requests": total_closed,
        "total_requests": total_requests,
        "average_resolution_time": average_resolution_time,
        "top_issue_types": top_issue_types,
        "sla_breach_count": sla_breach_count,
        "completion_rate": completion_rate
    }


@router.get("/requests-by-status")
async def get_requests_by_status(db: AsyncSession = Depends(get_db)) -> List[Dict[str, Any]]:
    """Get count of requests grouped by status."""
    query = select(
        DBRequest.status.label('status'),
        func.count().label('count')
    ).group_by(DBRequest.status).order_by(func.count().desc())
    
    result = await db.execute(query)
    return [
        {"status": str(row.status), "count": row.count}
        for row in result.fetchall()
    ]


@router.get("/requests-by-priority")
async def get_requests_by_priority(db: AsyncSession = Depends(get_db)) -> List[Dict[str, Any]]:
    """Get count of requests grouped by priority."""
    query = select(
        DBRequest.priority.label('priority'),
        func.count().label('count')
    ).group_by(DBRequest.priority).order_by(func.count().desc())
    
    result = await db.execute(query)
    return [
        {"priority": str(row.priority), "count": row.count}
        for row in result.fetchall()
    ]


@router.get("/requests-over-time")
async def get_requests_over_time(days: int = 30, db: AsyncSession = Depends(get_db)) -> List[Dict[str, Any]]:
    """Get count of requests created over time."""
    start_date = datetime.utcnow() - timedelta(days=days)
    
    query = select(
        func.date(DBRequest.created_at).label('date'),
        func.count().label('count')
    ).where(
        DBRequest.created_at >= start_date
    ).group_by(func.date(DBRequest.created_at)).order_by(func.date(DBRequest.created_at))
    
    result = await db.execute(query)
    return [
        {"date": str(row.date), "count": row.count}
        for row in result.fetchall()
    ]


@router.get("/building-performance")
async def get_building_performance(db: AsyncSession = Depends(get_db)) -> List[Dict[str, Any]]:
    """Get performance metrics by building."""
    query = select(
        DBRequest.building_id,
        DBBuilding.name.label('building_name'),
        func.count().label('total_requests'),
        func.sum(
            case(
                (DBRequest.status.in_([RequestStatus.OPEN, RequestStatus.IN_PROGRESS]), 1),
                else_=0
            )
        ).label('open_requests'),
        func.sum(
            case(
                (DBRequest.status.in_([RequestStatus.CLOSED, RequestStatus.COMPLETED]), 1),
                else_=0
            )
        ).label('closed_requests')
    ).join(
        DBBuilding, DBRequest.building_id == DBBuilding.id
    ).group_by(
        DBRequest.building_id, DBBuilding.name
    ).order_by(func.count().desc())
    
    result = await db.execute(query)
    return [
        {
            "_id": row.building_id,
            "building_name": row.building_name,
            "total_requests": row.total_requests,
            "open_requests": row.open_requests,
            "closed_requests": row.closed_requests
        }
        for row in result.fetchall()
    ]


@router.get("/staff-performance")
async def get_staff_performance(db: AsyncSession = Depends(get_db)) -> List[Dict[str, Any]]:
    """Get performance metrics by staff member."""
    # Get all requests with assignments
    query = select(DBRequest.assignments, DBRequest.id).where(DBRequest.assignments.is_not(None))
    result = await db.execute(query)
    requests = result.fetchall()
    
    # Process assignments
    staff_stats = {}
    for row in requests:
        if not row.assignments:
            continue
        for assignment in row.assignments:
            staff_id = assignment.get("staff_id")
            if not staff_id:
                continue
            
            if staff_id not in staff_stats:
                staff_stats[staff_id] = {
                    "total_assignments": 0,
                    "completed_assignments": 0,
                    "active_assignments": 0
                }
            
            staff_stats[staff_id]["total_assignments"] += 1
            if assignment.get("completed_at"):
                staff_stats[staff_id]["completed_assignments"] += 1
            else:
                staff_stats[staff_id]["active_assignments"] += 1
    
    # Enrich with staff names
    results = []
    for staff_id, stats in staff_stats.items():
        staff_query = select(DBStaff).where(DBStaff.id == staff_id)
        staff_result = await db.execute(staff_query)
        staff = staff_result.scalar_one_or_none()
        
        results.append({
            "_id": staff_id,
            "staff_name": staff.full_name if staff else "Unknown",
            "staff_role": staff.role if staff else "Unknown",
            **stats
        })
    
    # Sort by total assignments
    results.sort(key=lambda x: x["total_assignments"], reverse=True)
    
    return results
