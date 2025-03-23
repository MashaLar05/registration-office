from sqlalchemy import Column, DateTime, Enum, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from .user_role import RoleEnum
from ..database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    last_name = Column(String)
    role = Column(Enum(RoleEnum), default=RoleEnum.USER)
    date_of_birth = Column(DateTime)

    appointments = relationship("Appointment", back_populates="user")
