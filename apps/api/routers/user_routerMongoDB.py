from fastapi import APIRouter, Body
from bson.objectid import ObjectId
from datetime import datetime
from ..connect_mongodb import users_collection

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/")
def create_user_endpoint(data=Body()):
    result = users_collection.insert_one({
        "name": data["name"],
        "last_name": data["last_name"],
        "role": data["role"],
        "date_of_birth": data["date_of_birth"]
    })
    user = users_collection.find_one({"_id": result.inserted_id})
    user["id"] = str(user["_id"])
    del user["_id"]
    return user


@router.get("/")
def get_user_endpoint():
    users = []
    for user in users_collection.find():
        user["id"] = str(user["_id"])
        del user["_id"]
        users.append(user)
    return users


@router.get("/{user_id}")
def get_user_by_id_endpoint(user_id: str):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user["id"] = str(user["_id"])
        del user["_id"]
        return user
    return {"message": "User not found"}


@router.put("/{user_id}")
def update_user_endpoint(user_id: str, data=Body()):
    users_collection.update_one({"_id": ObjectId(user_id)}, {
        "$set": {
            "name": data["name"],
            "last_name": data["last_name"],
            "role": data["role"],
            "date_of_birth": data["date_of_birth"]
        }
    })
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user["id"] = str(user["_id"])
        del user["_id"]
        return user
    return {"message": "User not found"}


@router.delete("/{user_id}")
def delete_user_endpoint(user_id: str):
    result = users_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 1:
        return {"message": "User deleted"}
    return {"message": "User not found"}
