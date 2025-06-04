from bson import ObjectId
from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime

from db_connect import appointments_collection, doctors_collection, users_collection


def convert_objectid(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, ObjectId):
                obj[key] = str(value)
            elif isinstance(value, dict):
                obj[key] = convert_objectid(value)
            elif isinstance(value, list):
                obj[key] = [convert_objectid(v) if isinstance(
                    v, (dict, ObjectId)) else v for v in value]
    elif isinstance(obj, ObjectId):
        return str(obj)
    return obj


@csrf_exempt
def all_appointments(request):

    if request.method == "GET":
        # id -> name
        user_map = {str(user["_id"]): user["name"]
                    for user in users_collection.find()}
        doctor_map = {str(doctor["_id"]): doctor["name"]
                      for doctor in doctors_collection.find()}
        if request.headers.get("Accept") == "application/json":
            appointments = []
            for appointment in appointments_collection.find():
                appointment["id"] = str(appointment["_id"])

                appointment["user"] = user_map.get(
                    str(appointment["user_id"]), "Unknown")
                appointment["doctor"] = doctor_map.get(
                    str(appointment["doctor_id"]), "Unknown")

                del appointment["_id"]
                appointments.append(convert_objectid(appointment))
            return JsonResponse(appointments, safe=False)
        else:
            return render(request, "appointments_entity.html", {"table_name": "appointments"})

    elif request.method == "POST":
        # name -> id
        user_map = {user["name"]: str(user["_id"])
                    for user in users_collection.find()}
        doctor_map = {doctor["name"]: str(doctor["_id"])
                      for doctor in doctors_collection.find()}
        data = json.loads(request.body)
        raw_date = data.get("date_time", "")
        try:
            formatted_date = datetime.fromisoformat(raw_date).isoformat()
        except ValueError:
            formatted_date = ""

        user_name = data.get("user", "")
        doctor_name = data.get("doctor", "")

        user_id = user_map.get(user_name)
        doctor_id = doctor_map.get(doctor_name)

        if not user_id or not doctor_id:
            return JsonResponse({"error": "Invalid user or doctor name"}, status=400)

        new_appointment = appointments_collection.insert_one({
            "user_id": ObjectId(user_id),
            "doctor_id": ObjectId(doctor_id),
            "date_time": formatted_date
        })
        appointment = appointments_collection.find_one(
            {"_id": new_appointment.inserted_id})
        appointment["id"] = str(appointment["_id"])
        appointment["user"] = user_name
        appointment["doctor"] = doctor_name
        try:
            dt = datetime.fromisoformat(appointment["date_time"])
            appointment["date_time"] = dt.strftime("%Y-%m-%d %H:%M")
        except Exception:
            pass
        del appointment["_id"]
        appointment = convert_objectid(appointment)
        return JsonResponse(appointment)


@csrf_exempt
def appointment_detail(request, appointment_id):
    try:
        id = ObjectId(appointment_id)
    except:
        return JsonResponse({"message": "Invalid ID format"}, status=400)

    appointment = appointments_collection.find_one({"_id": id})
    if not appointment:
        return HttpResponseNotFound(json.dumps({"message": "Appointment not found"}), content_type="application/json")

    users = list(users_collection.find())
    doctors = list(doctors_collection.find())

    # name -> id
    user_map_name = {user["name"]: str(user["_id"])
                     for user in users}
    doctor_map_name = {doctor["name"]: str(doctor["_id"])
                       for doctor in doctors}

    # id -> name
    user_map_id = {str(user["_id"]): user["name"]
                   for user in users}
    doctor_map_id = {str(doctor["_id"]): doctor["name"]
                     for doctor in doctors}

    if request.method == "GET":
        appointment["id"] = str(appointment["_id"])
        appointment["user"] = user_map_id.get(
            str(appointment["user_id"]), "Unknown")
        appointment["doctor"] = doctor_map_id.get(
            str(appointment["doctor_id"]), "Unknown")
        del appointment["_id"]
        appointment = convert_objectid(appointment)
        return JsonResponse(appointment)

    elif request.method == "PUT":
        data = json.loads(request.body)
        raw_date = data.get("date_time", "")
        try:
            formatted_date = datetime.fromisoformat(raw_date).isoformat()
        except ValueError:
            formatted_date = appointment["date_time"]

        user_name = data.get("user", "")
        doctor_name = data.get("doctor", "")

        user_id = user_map_name.get(user_name)
        doctor_id = doctor_map_name.get(doctor_name)

        if not user_id or not doctor_id:
            return JsonResponse({"error": "Invalid user or doctor name"}, status=400)

        appointments_collection.update_one({"_id": id}, {
            "$set": {
                "user_id": ObjectId(user_id),
                "doctor_id": ObjectId(doctor_id),
                "date_time": formatted_date
            }
        })

        appointment = appointments_collection.find_one({"_id": id})
        appointment["id"] = str(appointment["_id"])
        appointment["user"] = user_name
        appointment["doctor"] = doctor_name
        try:
            dt = datetime.fromisoformat(appointment["date_time"])
            appointment["date_time"] = dt.strftime("%Y-%m-%d %H:%M")
        except Exception:
            pass
        del appointment["_id"]
        appointment = convert_objectid(appointment)
        return JsonResponse(appointment)

    elif request.method == "DELETE":
        result = appointments_collection.delete_one({"_id": id})
        if result.deleted_count == 1:
            return JsonResponse({"message": "Appointment deleted", "id": appointment_id})
        else:
            return JsonResponse({"message": "Appointment not found"}, status=404)


@csrf_exempt
def user_appointments(request):
    user = request.session.get("user")
    if not user or user["role"] != "user":
        return JsonResponse({"error": "Unauthorized"}, status=401)

    if request.method == "GET":
        appointments = []
        for appointment in appointments_collection.find({"user_id": user["id"]}):
            user_data = users_collection.find_one(
                {"_id": ObjectId(appointment["user_id"])})
            doctor_data = doctors_collection.find_one(
                {"_id": ObjectId(appointment["doctor_id"])})
            appointments.append({
                "id": str(appointment["_id"]),
                "user_id": appointment["user_id"],
                "user_name": f"{user_data['name']} {user_data['last_name']}" if user_data else "Unknown",
                "doctor_id": appointment["doctor_id"],
                "doctor_name": f"{doctor_data['name']} {doctor_data['last_name']}" if doctor_data else "Unknown",
                "date_time": appointment["date_time"]
            })
        return JsonResponse(appointments, safe=False)

    elif request.method == "POST":
        data = json.loads(request.body)
        user_id = data.get("user_id")
        doctor_id = data.get("doctor_id")
        date_time = data.get("date_time")

        if not all([user_id, doctor_id, date_time]):
            return JsonResponse({"error": "All fields are required"}, status=400)

        if user_id != user["id"]:
            return JsonResponse({"error": "Cannot create appointment for another user"}, status=403)

        try:
            ObjectId(doctor_id)
        except:
            return JsonResponse({"error": "Invalid doctor_id"}, status=400)

        if not doctors_collection.find_one({"_id": ObjectId(doctor_id)}):
            return JsonResponse({"error": "Doctor not found"}, status=404)

        try:
            datetime.fromisoformat(date_time.replace("Z", ""))
        except ValueError:
            return JsonResponse({"error": "Invalid date_time format"}, status=400)

        new_appointment = appointments_collection.insert_one({
            "user_id": user_id,  # Сохраняем как строку
            "doctor_id": doctor_id,  # Сохраняем как строку
            "date_time": date_time
        })

        appointment = appointments_collection.find_one(
            {"_id": new_appointment.inserted_id})
        user_data = users_collection.find_one(
            {"_id": ObjectId(appointment["user_id"])})
        doctor_data = doctors_collection.find_one(
            {"_id": ObjectId(appointment["doctor_id"])})
        return JsonResponse({
            "id": str(appointment["_id"]),
            "user_id": appointment["user_id"],
            "user_name": f"{user_data['name']} {user_data['last_name']}" if user_data else "Unknown",
            "doctor_id": appointment["doctor_id"],
            "doctor_name": f"{doctor_data['name']} {doctor_data['last_name']}" if doctor_data else "Unknown",
            "date_time": appointment["date_time"]
        })


@csrf_exempt
def user_appointment_detail(request, appointment_id):
    user = request.session.get("user")
    if not user or user["role"] != "user":
        return JsonResponse({"error": "Unauthorized"}, status=401)

    try:
        appointment_id = ObjectId(appointment_id)
    except:
        return JsonResponse({"error": "Invalid ID format"}, status=400)

    appointment = appointments_collection.find_one({"_id": appointment_id})
    if not appointment:
        return HttpResponseNotFound(json.dumps({"error": "Appointment not found"}), content_type="application/json")

    if appointment["user_id"] != user["id"]:
        return JsonResponse({"error": "Access denied"}, status=403)

    if request.method == "GET":
        user_data = users_collection.find_one(
            {"_id": ObjectId(appointment["user_id"])})
        doctor_data = doctors_collection.find_one(
            {"_id": ObjectId(appointment["doctor_id"])})
        return JsonResponse({
            "id": str(appointment["_id"]),
            "user_id": appointment["user_id"],
            "user_name": f"{user_data['name']} {user_data['last_name']}" if user_data else "Unknown",
            "doctor_id": appointment["doctor_id"],
            "doctor_name": f"{doctor_data['name']} {doctor_data['last_name']}" if doctor_data else "Unknown",
            "date_time": appointment["date_time"]
        })

    elif request.method == "PUT":
        data = json.loads(request.body)
        user_id = data.get("user_id")
        doctor_id = data.get("doctor_id")
        date_time = data.get("date_time")

        if not all([user_id, doctor_id, date_time]):
            return JsonResponse({"error": "All fields are required"}, status=400)

        if user_id != user["id"]:
            return JsonResponse({"error": "Cannot edit appointment for another user"}, status=403)

        try:
            ObjectId(doctor_id)
        except:
            return JsonResponse({"error": "Invalid doctor_id"}, status=400)

        if not doctors_collection.find_one({"_id": ObjectId(doctor_id)}):
            return JsonResponse({"error": "Doctor not found"}, status=404)

        try:
            datetime.fromisoformat(date_time.replace("Z", ""))
        except ValueError:
            return JsonResponse({"error": "Invalid date_time format"}, status=400)

        appointments_collection.update_one(
            {"_id": appointment_id},
            {"$set": {"user_id": user_id, "doctor_id": doctor_id, "date_time": date_time}}
        )

        appointment = appointments_collection.find_one({"_id": appointment_id})
        user_data = users_collection.find_one(
            {"_id": ObjectId(appointment["user_id"])})
        doctor_data = doctors_collection.find_one(
            {"_id": ObjectId(appointment["doctor_id"])})
        return JsonResponse({
            "id": str(appointment["_id"]),
            "user_id": appointment["user_id"],
            "user_name": f"{user_data['name']} {user_data['last_name']}" if user_data else "Unknown",
            "doctor_id": appointment["doctor_id"],
            "doctor_name": f"{doctor_data['name']} {doctor_data['last_name']}" if doctor_data else "Unknown",
            "date_time": appointment["date_time"]
        })

    elif request.method == "DELETE":
        result = appointments_collection.delete_one({"_id": appointment_id})
        if result.deleted_count == 1:
            return JsonResponse({"id": str(appointment_id)})
        return JsonResponse({"error": "Appointment not found"}, status=404)
