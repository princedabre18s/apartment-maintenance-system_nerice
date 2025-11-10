from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


# Building Models
class BuildingBase(BaseModel):
    name: str = Field(..., max_length=200)
    address: str
    neighborhood: Optional[str] = None
    city: str = "Boston"
    state: str = "MA"
    zip_code: Optional[str] = None


class BuildingCreate(BuildingBase):
    pass


class BuildingUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=200)
    address: Optional[str] = None
    neighborhood: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None


class Building(BuildingBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Unit Models
class UnitBase(BaseModel):
    building_id: str
    unit_number: str
    floor: Optional[int] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    square_feet: Optional[int] = None


class UnitCreate(UnitBase):
    pass


class UnitUpdate(BaseModel):
    building_id: Optional[str] = None
    unit_number: Optional[str] = None
    floor: Optional[int] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    square_feet: Optional[int] = None


class Unit(UnitBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Tenant Models
class EmergencyContact(BaseModel):
    name: str
    phone: str
    relationship: str


class TenantBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    unit_id: str
    move_in_date: Optional[datetime] = None
    lease_end_date: Optional[datetime] = None
    emergency_contact: Optional[EmergencyContact] = None


class TenantCreate(TenantBase):
    pass


class TenantUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    unit_id: Optional[str] = None
    move_in_date: Optional[datetime] = None
    lease_end_date: Optional[datetime] = None
    emergency_contact: Optional[EmergencyContact] = None


class Tenant(TenantBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Staff Models
class StaffBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    role: str
    specialties: Optional[List[str]] = []
    hire_date: Optional[datetime] = None
    active: bool = True


class StaffCreate(StaffBase):
    pass


class StaffUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    specialties: Optional[List[str]] = None
    hire_date: Optional[datetime] = None
    active: Optional[bool] = None


class Staff(StaffBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Request Models
class RequestStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    CLOSED = "CLOSED"


class Priority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    EMERGENCY = "Emergency"


class IssueType(str, Enum):
    PLUMBING = "Plumbing"
    ELECTRICAL = "Electrical"
    HVAC = "HVAC"
    APPLIANCES = "Appliances"
    CLEANING = "Cleaning"
    PEST_CONTROL = "Pest Control"
    SECURITY = "Security"
    STRUCTURAL = "Structural"
    OTHER = "Other"


class Assignment(BaseModel):
    staff_id: str
    assigned_at: datetime
    accepted_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    notes: Optional[str] = None


class Note(BaseModel):
    id: Optional[str] = None
    author_type: str  # "tenant" or "staff"
    author_id: str
    author_name: str
    body: str = Field(..., max_length=2000)
    created_at: datetime

    class Config:
        from_attributes = True


class LocationDetails(BaseModel):
    neighborhood: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class RequestBase(BaseModel):
    external_id: Optional[str] = None
    tenant_id: str
    unit_id: str
    building_id: str
    issue_type: IssueType
    priority: Priority
    description: str = Field(..., max_length=2000)
    target_sla_hours: int = Field(default=72, gt=0)
    location_details: Optional[LocationDetails] = None


class RequestCreate(RequestBase):
    status: RequestStatus = RequestStatus.OPEN


class RequestUpdate(BaseModel):
    issue_type: Optional[IssueType] = None
    priority: Optional[Priority] = None
    description: Optional[str] = Field(None, max_length=2000)
    status: Optional[RequestStatus] = None
    target_sla_hours: Optional[int] = Field(None, gt=0)
    resolution_notes: Optional[str] = None


class Request(RequestBase):
    id: str
    status: RequestStatus
    created_at: datetime
    updated_at: datetime
    closed_at: Optional[datetime] = None
    assignments: List[Assignment] = []
    notes: List[Note] = []
    resolution_notes: Optional[str] = None

    class Config:
        from_attributes = True


class AssignmentCreate(BaseModel):
    staff_id: str
    notes: Optional[str] = None


class NoteCreate(BaseModel):
    author_type: str
    author_id: str
    author_name: str
    body: str = Field(..., max_length=2000)
