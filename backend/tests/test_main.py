# Name: Krystal Lu (klu04)
# Citation for async testing
# Date: 04/20/2025
# Adapted from "FastAPI - Async Tests" and "asgi-lifespan"
# Source URL (1): https://fastapi.tiangolo.com/advanced/async-tests/
# Source URL (2): https://github.com/florimondmanca/asgi-lifespan#usage

import pytest
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.anyio
async def test_read_msg():
    async with LifespanManager(app):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Connected to database."}
