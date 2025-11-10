from .buildings import router as buildings_router
from .units import router as units_router
from .tenants import router as tenants_router
from .staff import router as staff_router
from .requests import router as requests_router
from .metrics import router as metrics_router

__all__ = [
    "buildings_router",
    "units_router",
    "tenants_router",
    "staff_router",
    "requests_router",
    "metrics_router"
]
