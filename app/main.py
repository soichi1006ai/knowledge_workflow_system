from fastapi import FastAPI

from app.api.routers.health import router as health_router
from app.api.routers.raw import router as raw_router
from app.api.routers.pages import router as pages_router
from app.api.routers.query import router as query_router
from app.api.routers.decisions import router as decisions_router
from app.api.routers.actions import router as actions_router
from app.api.routers.unresolved import router as unresolved_router
from app.api.routers.reviews import router as reviews_router
from app.api.routers.dashboard import router as dashboard_router

app = FastAPI(title="Knowledge Workflow System API", version="0.1.0")

app.include_router(health_router)
app.include_router(raw_router)
app.include_router(pages_router)
app.include_router(query_router)
app.include_router(decisions_router)
app.include_router(actions_router)
app.include_router(unresolved_router)
app.include_router(reviews_router)
app.include_router(dashboard_router)
