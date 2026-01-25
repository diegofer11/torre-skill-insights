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


@router.get("/{username}/skills")
async def get_user_skills(username: str):
    validate_username(username)

    client = TorreClient()
    try:
        genome = await client.get_user_genome(username)
        await client.close()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await client.close()

    strengths = genome.get("strengths", [])
    skills = [s.get("name") for s in strengths if "name" in s]

    return {"username": username, "skills": skills}
