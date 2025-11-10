import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_root():
    """Test root endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


@pytest.mark.asyncio
async def test_health_check():
    """Test health check endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_get_buildings():
    """Test get all buildings endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/buildings/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_metrics_overview():
    """Test metrics overview endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/metrics/overview")
    assert response.status_code == 200
    data = response.json()
    assert "total_open_requests" in data
    assert "total_closed_requests" in data
    assert "average_resolution_time" in data
    assert "top_issue_types" in data
    assert "sla_breach_count" in data
