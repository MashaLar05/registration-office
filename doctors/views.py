from bson import ObjectId
from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime

from db_connect import doctors_collection


@csrf_exempt
def all_doctors(request):
    if request.method == "GET":
        if request.headers.get("Accept") == "application/json":
            doctors = []
            for doctor in doctors_collection.find():
                doctor["id"] = str(doctor["_id"])
                del doctor["_id"]
                doctors.append(doctor)
            return JsonResponse(doctors, safe=False)
        else:
            return render(request, "doctors_entity.html", {"table_name": "Doctors"})

    elif request.method == "POST":
        data = json.loads(request.body)
        raw_date = data.get("date_of_birth", "")
        try:
            formatted_date = datetime.fromisoformat(raw_date).isoformat()
        except ValueError:
            formatted_date = ""

        new_doctor = doctors_collection.insert_one({
            "name": data.get("name", ""),
            "last_name": data.get("last_name", ""),
            "qualification": data.get("qualification", ""),
            "date_of_birth": formatted_date
        })

        doctor = doctors_collection.find_one({"_id": new_doctor.inserted_id})
        doctor["_id"] = str(doctor["_id"])
        del doctor["_id"]
        return JsonResponse(doctor)


@csrf_exempt
def doctor_detail(request, doctor_id):
    try:
        id = ObjectId(doctor_id)
    except:
        return JsonResponse({"message": "Invalid ID format"}, status=400)

    doctor = doctors_collection.find_one({"_id": id})
    if not doctor:
        return HttpResponseNotFound(json.dumps({"message": "Doctor not found"}), content_type="application/json")

    if request.method == "GET":
        doctor["_id"] = str(doctor["_id"])
        del doctor["_id"]
        return JsonResponse(doctor)

    elif request.method == "PUT":
        data = json.loads(request.body)
        raw_date = data.get("date_of_birth", "")
        try:
            formatted_date = datetime.fromisoformat(raw_date).isoformat()
        except ValueError:
            formatted_date = doctor["date_of_birth"]

        doctors_collection.update_one({"_id": id}, {
            "$set": {
                "name": data.get("name", doctor["name"]),
                "last_name": data.get("last_name", doctor["last_name"]),
                "qualification": data.get("qualification", doctor["qualification"]),
                "date_of_birth": formatted_date
            }
        })
        doctor = doctors_collection.find_one({"_id": id})
        doctor["_id"] = str(doctor["_id"])
        del doctor["_id"]
        return JsonResponse(doctor)

    elif request.method == "DELETE":
        result = doctors_collection.delete_one({"_id": id})
        if result.deleted_count == 1:
            return JsonResponse({"message": "Doctor deleted", "id": doctor_id})
        else:
            return JsonResponse({"message": "Doctor not found"}, status=404)
