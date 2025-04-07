from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from apps.api.database import get_db
from ..services.user_server import create_user, get_user, get_user_by_id, delete_user, update_user
from datetime import datetime

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/")
def create_user_endpoint(data = Body(), db: Session = Depends(get_db)):
    data["date_of_birth"] = datetime.fromisoformat(data["date_of_birth"])
    return create_user(data, db)

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
def update_user_endpoint(user_id: int, data = Body(), db: Session = Depends(get_db)):
    data["date_of_birth"] = datetime.fromisoformat(data["date_of_birth"])
    return update_user(user_id, data, db)

@router.delete("/{user_id}")
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    user = delete_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user_id}
