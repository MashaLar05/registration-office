from sqlalchemy import DateTime, create_engine, Column, Enum, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from .models.user_role import FirstRoleEnum, SecondRoleEnum
# from .models.models import user, appointments, doctors

DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

Base = declarative_base()


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    last_name = Column(String)
    web_role = Column(Enum(FirstRoleEnum), default=FirstRoleEnum.USER)
    role = Column(Enum(SecondRoleEnum), default=SecondRoleEnum.PATIENT)
    date_of_birth = Column(DateTime)
# YYYY-MM-DDTHH:MM:SS
    appointments = relationship("Appointment", back_populates="user")


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    last_name = Column(String)
    qualification = Column(String)
    date_of_birth = Column(DateTime)
    role = Column(Enum(FirstRoleEnum), default=SecondRoleEnum.DOCTOR)

    appointments = relationship("Appointment", back_populates="doctor")


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))

    user = relationship("User", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")


Base.metadata.create_all(bind=engine)
