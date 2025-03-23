from sqlalchemy.orm import Session
from ..models.user import User, User
from ..models.user_role import RoleEnum
from datetime import datetime

# create


def create_user(db: Session, user_name: str, user_last_name: str, user_role: RoleEnum, user_date_of_birth: datetime):
    db_user = User(name=user_name, last_name=user_last_name,
                   role=user_role, date_of_birth=user_date_of_birth)

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


def update_user(db: Session, curent_user_id: int, user_id: int, new_user_name: str, new_user_last_name: str, new_user_role: RoleEnum, new_user_date_of_birth: datetime):
    curent_user = db.query(User).filter(User.id == curent_user_id).first()

    if curent_user and curent_user.role == RoleEnum.ADMIN:
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            db_user.name = new_user_name
            db_user.last_name = new_user_last_name
            db_user.date_of_birth = new_user_date_of_birth
            if new_user_role != db_user.role:
                db_user.role = new_user_role
            db.commit()
            db.refresh(db_user)
        return db_user
    else:
        return None

# delete


def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
