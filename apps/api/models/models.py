from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
# from .user_role import RoleEnum
from ..database import Base


# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#     last_name = Column(String)
#     role = Column(Enum(RoleEnum), default=RoleEnum.USER)
#     date_of_birth = Column(DateTime)
# # YYYY-MM-DDTHH:MM:SS
#     appointments = relationship("Appointment", back_populates="user")


# class Doctor(Base):
#     __tablename__ = "doctors"

#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     last_name = Column(String)
#     qualification = Column(String)
#     date_of_birth = Column(DateTime)

#     appointments = relationship("Appointment", back_populates="doctor")


# class Appointment(Base):
#     __tablename__ = "appointments"

#     id = Column(Integer, primary_key=True, index=True)
#     date_time = Column(DateTime, nullable=False)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     doctor_id = Column(Integer, ForeignKey("doctors.id"))

#     user = relationship("User", back_populates="appointments")
#     doctor = relationship("Doctor", back_populates="appointments")
