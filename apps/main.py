from fastapi import Body, Depends, FastAPI, Query
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from datetime import datetime

from apps.api.services.user_server import get_user

from apps.api.routers.user_router import router as user_router
from apps.api.database import *


app = FastAPI()

app.include_router(user_router)

templates = Jinja2Templates(directory="apps/client/pages")
app.mount("/static", StaticFiles(directory="apps/client/styles"), name="static")


@app.get("/", tags=["Home"])
async def read_root(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})


# start app from console>> uvicorn apps.main:app --reload
