from fastapi import FastAPI
from app.api.user_router import router

app = FastAPI(title="Skill Insights Dashboard")
app.include_router(router)
