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


@pytest.mark.asyncio
async def test_get_user_skills_invalid_username_length():
    transport = httpx.ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(f"{URL_PREFIX}/users/_/skills")

    assert response.status_code == 400

    data = response.json()
    assert "Username must be at least 4 characters long." in data["detail"]


@pytest.mark.asyncio
async def test_get_user_skills_invalid_username_only_numbers(mocker):
    transport = httpx.ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(f"{URL_PREFIX}/users/1233/skills")

    assert response.status_code == 400

    data = response.json()
    assert "Username cannot be a number." in data["detail"]


@pytest.mark.asyncio
async def test_get_user_skills_invalid_username_spaces(mocker):
    transport = httpx.ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(f"{URL_PREFIX}/users/    /skills")

    assert response.status_code == 400

    data = response.json()
    assert "Username must be provided and cannot be empty." in data["detail"]
