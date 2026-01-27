from app.client.torre_client import TorreClient
from app.core.validators import validate_username
from app.services.user_skills_service import get_user_skills_service


async def get_user_insights_service(username: str, limit: int = 5) -> dict:
    """
    Fetches insights for the specified user based on their skills and related opportunities.
    The service interacts with user skills and opportunities data to generate a detailed
    insights dictionary.

    :param username: The username of the individual whose insights are to be fetched.
    :param limit: The maximum number of opportunities to fetch for each skill. Defaults to 5.
    :return: A dictionary containing the user's username, their skills, and insights which
             include opportunities related to each skill.
    """
    validate_username(username)
    client = TorreClient()
    try:
        user_data = await get_user_skills_service(username)
        skills = user_data["skills"]

        insights = {}
        for skill in skills:
            opportunities = await client.find_opportunities(skill, limit=limit)
            insights[skill] = opportunities.get("results", [])
    finally:
        await client.close()

    return {
        "username": username,
        "skills": skills,
        "insights": insights
    }
