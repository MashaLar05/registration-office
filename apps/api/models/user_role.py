from enum import Enum


class FirstRoleEnum(str, Enum):
    ADMIN = "admin"
    USER = "user"


class SecondRoleEnum(str, Enum):
    DOCTOR = "doctor"
    PATIENT = "patient"
    PRACTITIONER = "practitioner"
    NURSE = "nurse"
