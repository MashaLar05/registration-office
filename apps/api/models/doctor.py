from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from ..database import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    last_name = Column(String)
    qualification = Column(String)
    date_of_birth = Column(DateTime)

    appointments = relationship("Appointment", back_populates="doctor")
