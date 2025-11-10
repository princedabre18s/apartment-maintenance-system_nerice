from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .database import Database
from .config import settings
from .routers import buildings, units, tenants, staff, requests, metrics


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifespan events.
    Connect to MongoDB on startup and close connection on shutdown.
    """
    # Startup
    await Database.connect_db()
    print("Application startup complete")
    
    yield
    
    # Shutdown
    await Database.close_db()
    print("Application shutdown complete")


app = FastAPI(
    title="Apartment Maintenance Request System",
    description="A comprehensive system for managing apartment maintenance requests with MongoDB backend",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(buildings.router)
app.include_router(units.router)
app.include_router(tenants.router)
app.include_router(staff.router)
app.include_router(requests.router)
app.include_router(metrics.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Apartment Maintenance Request System API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.environment == "development"
    )
