from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.user_server import create_user, get_user, get_user_by_id, update_user, delete_user
from ..models.user_role import FirstRoleEnum, SecondRoleEnum
from datetime import datetime
from fastapi.requests import Request


router = APIRouter(prefix="/users", tags=["Users"])

templates = Jinja2Templates(directory="apps/client/pages")


class UserUpdateRequest(BaseModel):
    curent_user_id: int
    name: str
    last_name: str
    date_of_birth: datetime


@router.post("/")
def create_user_endpoint(
    name: str,
    last_name: str,
    web_role: FirstRoleEnum,
    role: SecondRoleEnum,
    date_of_birth: datetime,
    db: Session = Depends(get_db)
):
    return create_user(db, name, last_name, role, web_role, date_of_birth)


@router.get("/")
def get_user_endpoint(request: Request, db: Session = Depends(get_db)):
    users = get_user(db)
    return templates.TemplateResponse("all_users.html", {"request": request, "users": users})


@router.get("/{user_id}", response_class=HTMLResponse)
def get_user_by_id_endpoint(user_id: int, request: Request, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # return user
    return templates.TemplateResponse("user.html", {"request": request, "user": user})


# @router.put("/{user_id}")
# def update_user_endpoint(
#     user_id: int,
#     curent_user_id: int,
#     name: str,
#     last_name: str,
#     date_of_birth: datetime,
#     db: Session = Depends(get_db)
# ):
#     updated_user = update_user(
#         db, curent_user_id, user_id, name, last_name, date_of_birth)
#     if not updated_user:
#         raise HTTPException(
#             status_code=403, detail="Permission denied or user not found")
#     return updated_user

@router.put("/{user_id}")
def update_user_endpoint(
    user_id: int,
    update_data: UserUpdateRequest,
    db: Session = Depends(get_db)
):
    curent_user_id = update_data.curent_user_id
    name = update_data.name
    last_name = update_data.last_name
    date_of_birth = update_data.date_of_birth

    updated_user = update_user(
        db, curent_user_id, user_id, name, last_name, date_of_birth)
    if not updated_user:
        raise HTTPException(
            status_code=403, detail="Permission denied or user not found")
    return updated_user


@router.delete("/{user_id}")
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    user = delete_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}
