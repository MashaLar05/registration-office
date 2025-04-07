from sqlalchemy.orm import Session
from ..models.user import User
from fastapi.responses import JSONResponse

# create
def create_user(data, db):
    db_user = User(name=data["name"], last_name=data["last_name"],
                   role=data["role"], date_of_birth=data["date_of_birth"])

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# get
def get_user(db: Session):
    return db.query(User).all()

# get by id
def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# update
def update_user(user_id, data, db):
    user = db.query(User).filter(User.id == user_id).first()
    if user == None:
        return JSONResponse(status_code=404, content={"message": "Користувач не знайдений"})
    user.name = data["name"]
    user.last_name = data["last_name"]
    user.role = data["role"]
    user.date_of_birth = data["date_of_birth"]
    db.commit()
    db.refresh(user)
    return user

# delete
def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
