from sqlalchemy import Column, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from apps.api.database import Base

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))

    user = relationship("User", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")
