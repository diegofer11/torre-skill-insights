from typing import Optional

from fastapi import APIRouter
from fastapi.params import Query

from app.core.constants import URL_PREFIX
from app.services.user_insights_service import get_user_insights_service
from app.services.user_skills_service import get_user_skills_service

router = APIRouter(prefix=f"{URL_PREFIX}/users")


@router.get("/{username}/skills")
async def get_user_skills(username: str):
    return await get_user_skills_service(username)


@router.get("/{username}/insights")
async def get_user_insights(
        username: str,
        limit: Optional[int] = Query(5, description="Maximum number of opportunities to fetch per skill"),
        currency: Optional[str] = Query("USD", description="Reference currency: USD, EUR, GBP, JPY"),
        periodicity: Optional[str] = Query("hourly", description="Periodicity: hourly, daily, weekly, monthly"),
        lang: Optional[str] = Query("en", description="Language"),
        context_feature: Optional[str] = Query("job_feed", description="Search context"),
        criteria: str = Query("AND", description="Search criteria operator: AND, OR")
):
    return await get_user_insights_service(
        username=username,
        limit=limit,
        currency=currency,
        periodicity=periodicity,
        lang=lang,
        context_feature=context_feature,
        criteria=criteria)
