from fastapi import FastAPI

from routers.system import router as system_router
from routers.auth import router as auth_router

app = FastAPI()

app.include_router(system_router)
app.include_router(auth_router)