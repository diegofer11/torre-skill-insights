from fastapi import APIRouter, HTTPException

from app.client.torre_client import TorreClient
from app.core.constants import URL_PREFIX

router = APIRouter(prefix=f"{URL_PREFIX}/users")


@router.get("/{username}/skills")
async def get_user_skills(username: str):
    client = TorreClient()
    try:
        genome = await client.get_user_genome(username)
        await client.close()
    except Exception as e:
        await client.close()
        raise HTTPException(status_code=400, detail=str(e))

    strengths = genome.get("strengths", [])
    skills = [s.get("name") for s in strengths if "name" in s]

    return {"username": username, "skills": skills}
