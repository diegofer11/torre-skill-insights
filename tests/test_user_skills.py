import pytest
from app.client.torre_client import TorreClient


@pytest.mark.asyncio
async def test_get_user_skills(mocker, test_client):
    mock_genome = {"strengths": [{"name": "Python"}, {"name": "FastAPI"}]}
    mocker.patch.object(TorreClient, "get_user_genome", return_value=mock_genome)

    async with test_client as ac:
        response = await ac.get("/api/v1/users/testuser/skills")

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert set(data["skills"]) == {"Python", "FastAPI"}


@pytest.mark.asyncio
async def test_get_user_skills_invalid_username_length(test_client):
    async with test_client as ac:
        response = await ac.get("/api/v1/users/_/skills")

    assert response.status_code == 400
    assert response.json()["detail"] == "Username must be at least 4 characters long."


@pytest.mark.asyncio
async def test_get_user_skills_invalid_username_only_numbers(test_client):
    async with test_client as ac:
        response = await ac.get("/api/v1/users/1233/skills")

    assert response.status_code == 400
    assert response.json()["detail"] == "Username cannot be a number."


@pytest.mark.asyncio
async def test_get_user_skills_invalid_username_spaces(test_client):
    async with test_client as ac:
        response = await ac.get("/api/v1/users/    /skills")

    assert response.status_code == 400
    assert response.json()["detail"] == "Username must be provided and cannot be empty."
