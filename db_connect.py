from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["registrationoffice"]

users_collection = db["users"]
doctors_collection = db["doctors"]
appointments_collection = db["appointments"]
