from typing import Optional

from fastapi import HTTPException
from httpx import HTTPStatusError

from app.client.torre_client import TorreClient
from app.core.validators import validate_username
from app.services.user_skills_service import get_user_skills_service


async def get_user_insights_service(
        username: str,
        limit: Optional[int] = None,
        currency: Optional[str] = None,
        periodicity: Optional[str] = None,
        lang: Optional[str] = None,
        context_feature: Optional[str] = None,
        criteria: Optional[str] = None
) -> dict:
    """
    Fetches insights for the specified user based on their skills and related opportunities.
    The service interacts with user skills and opportunities data to generate a detailed
    insights dictionary.

    :param username: The username of the individual whose insights are to be fetched.
    :param limit: The maximum number of opportunities to fetch for each skill. Defaults to 5.
    :param currency:
    :param periodicity:
    :param lang:
    :param context_feature:
    :param criteria:
    :return: A dictionary containing the user's username, their skills, and insights which
             include opportunities related to each skill.
    """
    validate_username(username)
    client = TorreClient()
    try:
        user_data = await get_user_skills_service(username)
        skills = user_data.get("skills", [])

        opportunities = await client.find_opportunities(
            skills,
            limit=limit,
            currency=currency,
            periodicity=periodicity,
            lang=lang,
            context_feature=context_feature,
            criteria=criteria
        )

        insights = {
            "opportunities": opportunities.get("results", []),
            "total": opportunities.get("total", 0)
        }
    except HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code,
                            detail=e.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
    finally:
        await client.close()

    return {
        "username": username,
        "skills": skills,
        "insights": insights
    }
