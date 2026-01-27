from fastapi import APIRouter

from app.core.constants import URL_PREFIX
from app.services.user_insights_service import get_user_insights_service
from app.services.user_skills_service import get_user_skills_service

router = APIRouter(prefix=f"{URL_PREFIX}/users")


@router.get("/{username}/skills")
async def get_user_skills(username: str):
    return await get_user_skills_service(username)


@router.get("/{username}/insights")
async def get_user_insights(username: str):
    return await get_user_insights_service(username)
