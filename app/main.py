from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Skill Insights Dashboard")
app.include_router(router)
