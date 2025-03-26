from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from apps.api.database import get_db
from ..services.user_server import create_user, get_user, get_user_by_id, update_user, delete_user
from ..models.user_role import RoleEnum
from datetime import datetime

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/")
def create_user_endpoint(
    name: str,
    last_name: str,
    role: RoleEnum,
    date_of_birth: datetime,
    db: Session = Depends(get_db)
):
    return create_user(db, name, last_name, role, date_of_birth)


@router.get("/")
def get_user_endpoint(db: Session = Depends(get_db)):
    return get_user(db)


@router.get("/{user_id}")
def get_user_by_id_endpoint(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}")
def update_user_endpoint(
    user_id: int,
    curent_user_id: int,
    name: str,
    last_name: str,
    role: RoleEnum,
    date_of_birth: datetime,
    db: Session = Depends(get_db)
):
    updated_user = update_user(
        db, curent_user_id, user_id, name, last_name, role, date_of_birth)
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
