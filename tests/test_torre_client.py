from unittest.mock import Mock, AsyncMock

import httpx
import pytest

from app.core.constants import BASE_GENOME_URL, BASE_OPPORTUNITIES_URL
from app.services.torre_client import TorreClient


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
    skill = "Python"
    mock_json_response = {"results": [{"id": "job1", "title": "Backend Developer"}]}

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.raise_for_status = Mock()
    mock_response.json.return_value = mock_json_response

    mocker.patch.object(httpx.AsyncClient, "post", new=AsyncMock(return_value=mock_response))

    result = await client.find_opportunities(skill, limit=5)

    httpx.AsyncClient.post.assert_called_once_with(
        f"{BASE_OPPORTUNITIES_URL}?size=5",
        json={
            "and":
                [
                    {"skill/role":
                        {
                            "text": skill,
                            "proficiency": "expert"
                        }
                    },
                    {
                        "status":
                            {
                                "code": "open"
                            }
                    }
                ]
        }
    )
    assert result == mock_json_response

    await client.close()


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
