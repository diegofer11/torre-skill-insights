import httpx
import pytest
from httpx import AsyncClient
from app.core.constants import URL_PREFIX

from app.main import app

torre_client = "app.client.torre_client.TorreClient"


@pytest.mark.asyncio
async def test_get_user_skills(mocker):
    mock_genome = {"strengths": [{"name": "Python"}, {"name": "FastAPI"}]}
    mocker.patch(f"{torre_client}.get_user_genome", return_value=mock_genome)
    transport = httpx.ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(f"{URL_PREFIX}/users/testuser/skills")

    assert response.status_code == 200

    data = response.json()
    assert data["username"] == "testuser"
    assert "Python" in data["skills"]
    assert "FastAPI" in data["skills"]
