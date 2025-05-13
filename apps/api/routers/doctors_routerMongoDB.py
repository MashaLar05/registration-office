from fastapi import APIRouter, Body
from bson.objectid import ObjectId
from datetime import datetime
from ..connect_mongodb import doctors_collection

router = APIRouter(prefix="/doctors", tags=["Doctors"])


@router.post("/")
def create_doctor_endpoint(data=Body()):
    result = doctors_collection.insert_one({
        "name": data["name"],
        "last_name": data["last_name"],
        "qualification": data["qualification"],
        "date_of_birth": data["date_of_birth"]
    })
    doctor = doctors_collection.find_one({"_id": result.inserted_id})
    doctor["id"] = str(doctor["_id"])
    del doctor["_id"]
    return doctor


@router.get("/")
def get_doctor_endpoint():
    doctors = []
    for doctor in doctors_collection.find():
        doctor["id"] = str(doctor["_id"])
        del doctor["_id"]
        doctors.append(doctor)
    return doctors


@router.get("/{doctor_id}")
def get_doctor_by_id_endpoint(doctor_id: str):
    doctor = doctors_collection.find_one({"_id": ObjectId(doctor_id)})
    if doctor:
        doctor["id"] = str(doctor["_id"])
        del doctor["_id"]
        return doctor
    return {"message": "doctor not found"}


@router.put("/{doctor_id}")
def update_doctor_endpoint(doctor_id: str, data=Body()):
    doctors_collection.update_one({"_id": ObjectId(doctor_id)}, {
        "$set": {
            "name": data["name"],
            "last_name": data["last_name"],
            "qualification": data["qualification"],
            "date_of_birth": data["date_of_birth"]
        }
    })
    doctor = doctors_collection.find_one({"_id": ObjectId(doctor_id)})
    if doctor:
        doctor["id"] = str(doctor["_id"])
        del doctor["_id"]
        return doctor
    return {"message": "doctor not found"}


@router.delete("/{doctor_id}")
def delete_doctor_endpoint(doctor_id: str):
    result = doctors_collection.delete_one({"_id": ObjectId(doctor_id)})
    if result.deleted_count == 1:
        return {"message": "doctor deleted"}
    return {"message": "doctor not found"}
