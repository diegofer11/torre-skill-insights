from fastapi import APIRouter, HTTPException

from app.client.torre_client import TorreClient
from app.core.constants import URL_PREFIX

router = APIRouter(prefix=f"{URL_PREFIX}/users")


def validate_username(username) -> None:
    if not username.strip():
        raise HTTPException(status_code=400, detail="Username must be provided and cannot be empty.")
    if len(username) < 4:
        raise HTTPException(status_code=400, detail="Username must be at least 4 characters long.")
    if username.isdigit():
        raise HTTPException(status_code=400, detail="Username cannot be a number.")


async def fetch_user_skills(client: TorreClient, username: str) -> list[str]:
    genome = await client.get_user_genome(username)
    strengths = genome.get("strengths", [])
    return [s.get("name") for s in strengths if "name" in s]


@router.get("/{username}/skills")
async def get_user_skills(username: str):
    validate_username(username)

    client = TorreClient()
    try:
        skills = await fetch_user_skills(client, username)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await client.close()

    return {"username": username, "skills": skills}


@router.get("/{username}/insights")
async def get_user_insights(username: str):
    validate_username(username)
    client = TorreClient()

    skills = await fetch_user_skills(client, username)

    insights = {}
    try:
        for skill in skills:
            opportunities = await client.find_opportunities(skill, limit=2)
            print(opportunities)
            insights[skill] = opportunities.get("results", [])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await client.close()

    return {
        "username": username,
        "skills": skills,
        "insights": insights
    }
