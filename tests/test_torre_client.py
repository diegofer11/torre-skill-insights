from unittest.mock import Mock, AsyncMock

import httpx
import pytest

from app.core.constants import BASE_GENOME_URL, BASE_OPPORTUNITIES_URL
from app.client.torre_client import TorreClient
from app.main import app


@pytest.mark.asyncio
async def test_get_user_genome_success(mocker):
    client = TorreClient()
    username = "testuser"
    mock_json_response = {"name": "Test User", "professionalHeadline": "Software Developer"}

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = Mock()
    mock_response.json.return_value = mock_json_response

    mock_get = mocker.patch.object(httpx.AsyncClient, "get", new=AsyncMock(return_value=mock_response))

    result = await client.get_user_genome(username)

    mock_get.assert_called_once_with(f"{BASE_GENOME_URL}/{username}")
    assert result == mock_json_response

    await client.close()


@pytest.mark.asyncio
async def test_find_opportunities_success(mocker):
    client = TorreClient()
    skills = ["Python"]
    mock_json_response = {"results": [{"id": "job1", "title": "Backend Developer"}]}

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.raise_for_status = Mock()
    mock_response.json.return_value = mock_json_response

    mocker.patch.object(httpx.AsyncClient, "post", new=AsyncMock(return_value=mock_response))

    result = await client.find_opportunities(skills, limit=5)

    httpx.AsyncClient.post.assert_called_once_with(
        BASE_OPPORTUNITIES_URL,
        headers={"Accept": "application/json", "Content-Type": "application/json",
                 "User-Agent": "PostmanRuntime/7.51.0"},
        params={"size": 5},
        json={"or": [{"skill/role": {"text": "Python", "proficiency": "expert"}}, {"status": {"code": "open"}}]})

    assert result == mock_json_response

    await (client.close())


@pytest.mark.asyncio
async def test_find_opportunities_http_error(mocker):
    client = TorreClient()
    skill = "Python"

    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Not Found",
        request=Mock(),
        response=Mock(status_code=404)
    )

    mocker.patch.object(httpx.AsyncClient, "post", new=AsyncMock(return_value=mock_response))

    with pytest.raises(httpx.HTTPStatusError):
        await client.find_opportunities(skill, limit=5)
        await client.close()


@pytest.mark.asyncio
async def test_find_opportunities_invalid_json(mocker):
    client = TorreClient()
    skill = "Python"

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.raise_for_status = Mock()
    mock_response.json.side_effect = ValueError("Invalid JSON")

    mocker.patch.object(httpx.AsyncClient, "post", new=AsyncMock(return_value=mock_response))

    with pytest.raises(ValueError):
        await client.find_opportunities(skill, limit=5)

    await client.close()


@pytest.mark.asyncio
async def test_get_user_insights_success(mocker):
    mock_genome = {"strengths": [{"name": "Python"}, {"name": "FastAPI"}]}
    mock_opportunities = {"results": [{"skills": [{"name": "Python"}, {"name": "Django"}]}]}

    mocker.patch("app.client.torre_client.TorreClient.get_user_genome", return_value=mock_genome)
    mocker.patch("app.client.torre_client.TorreClient.find_opportunities", return_value=mock_opportunities)

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="https://test") as ac:
        response = await ac.get("/api/v1/users/testuser/insights")

    assert response.status_code == 200
    data = response.json()

    # Assertions on username and skills
    assert data["username"] == "testuser"
    assert "Python" in data["skills"]
    assert "FastAPI" in data["skills"]

    # Assertions on insights
    assert any("Django" in [s["name"] for s in opp["skills"]] for opp in data["insights"]["opportunities"])
