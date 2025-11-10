from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, Text, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..database import Base


class RequestStatus(str, enum.Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    CLOSED = "CLOSED"


class Priority(str, enum.Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    EMERGENCY = "Emergency"


class IssueType(str, enum.Enum):
    PLUMBING = "Plumbing"
    ELECTRICAL = "Electrical"
    HVAC = "HVAC"
    APPLIANCES = "Appliances"
    CLEANING = "Cleaning"
    PEST_CONTROL = "Pest Control"
    SECURITY = "Security"
    STRUCTURAL = "Structural"
    OTHER = "Other"


class Building(Base):
    __tablename__ = "buildings"

    id = Column(String, primary_key=True)
    name = Column(String(200), nullable=False)
    address = Column(Text, nullable=False)
    neighborhood = Column(String(200))
    city = Column(String(100), default="Boston")
    state = Column(String(10), default="MA")
    zip_code = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    units = relationship("Unit", back_populates="building", cascade="all, delete-orphan")
    requests = relationship("Request", back_populates="building")


class Unit(Base):
    __tablename__ = "units"

    id = Column(String, primary_key=True)
    building_id = Column(String, ForeignKey("buildings.id", ondelete="CASCADE"), nullable=False)
    unit_number = Column(String(50), nullable=False)
    floor = Column(Integer)
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    square_feet = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    building = relationship("Building", back_populates="units")
    tenants = relationship("Tenant", back_populates="unit")
    requests = relationship("Request", back_populates="unit")


class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(String, primary_key=True)
    unit_id = Column(String, ForeignKey("units.id", ondelete="SET NULL"))
    full_name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    phone = Column(String(20))
    move_in_date = Column(DateTime)
    move_out_date = Column(DateTime)
    lease_start_date = Column(DateTime)
    lease_end_date = Column(DateTime)
    emergency_contact = Column(JSON)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    unit = relationship("Unit", back_populates="tenants")
    requests = relationship("Request", back_populates="tenant")


class Staff(Base):
    __tablename__ = "staff"

    id = Column(String, primary_key=True)
    full_name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    phone = Column(String(20))
    role = Column(String(100))
    specialties = Column(JSON)
    hire_date = Column(DateTime)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Request(Base):
    __tablename__ = "requests"

    id = Column(String, primary_key=True)
    external_id = Column(String(100))
    tenant_id = Column(String, ForeignKey("tenants.id", ondelete="SET NULL"), nullable=False)
    unit_id = Column(String, ForeignKey("units.id", ondelete="SET NULL"), nullable=False)
    building_id = Column(String, ForeignKey("buildings.id", ondelete="SET NULL"), nullable=False)
    issue_type = Column(SQLEnum(IssueType), nullable=False)
    priority = Column(SQLEnum(Priority), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(SQLEnum(RequestStatus), default=RequestStatus.OPEN)
    target_sla_hours = Column(Integer, default=72)
    location_details = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    closed_at = Column(DateTime)
    assignments = Column(JSON, default=list)
    notes = Column(JSON, default=list)
    resolution_notes = Column(Text)

    # Relationships
    tenant = relationship("Tenant", back_populates="requests")
    unit = relationship("Unit", back_populates="requests")
    building = relationship("Building", back_populates="requests")
