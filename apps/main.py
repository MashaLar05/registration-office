from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from apps.api.routers.user_router import router as user_router

app = FastAPI()

app.include_router(user_router)

templates = Jinja2Templates(directory="apps/client/pages")
app.mount("/static", StaticFiles(directory="apps/client/styles"), name="static")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})


@app.get("/entities/{table_name}")
async def get_entities_page(request: Request, table_name: str):
    return templates.TemplateResponse(
        "entities.html", {"request": request, "table_name": table_name}
    )
# start app from console>> uvicorn apps.main:app --reload
