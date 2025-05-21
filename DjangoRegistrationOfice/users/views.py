from django.http import JsonResponse, HttpResponseNotFound, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
from datetime import datetime

users = [
    {"id": "1",
     "name": "Nick",
     "last_name": "Nicks",
     "role": "user",
     "date_of_birth": "2000-01-03"},
    {"id": "2",
     "name": "El",
     "last_name": "Ele",
     "role": "admin",
     "date_of_birth": "2020-02-04"},
]


def find_user(user_id):
    user_id = str(user_id)
    for user in users:
        if user["id"] == user_id:
            return user
    return None


@csrf_exempt
def all_users(request):
    if request.method == "GET":
        if request.headers.get("Accept") == "application/json":
            return JsonResponse(users, safe=False)
        else:
            return render(request, "entities.html", {"table_name": "Users"})
    elif request.method == "POST":
        data = json.loads(request.body)
        new_user = {
            "id": str(uuid.uuid4()),
            "name": data.get("name", ""),
            "last_name": data.get("last_name", ""),
            "role": data.get("role", ""),
            "date_of_birth": data.get("date_of_birth", "")
        }
        users.append(new_user)
        return JsonResponse(new_user)


@csrf_exempt
def user_detail(request, user_id):
    user = find_user(user_id)
    if not user:
        return HttpResponseNotFound(json.dumps({"message": "User not found"}), content_type="application/json")

    if request.method == "GET":
        return JsonResponse(user)

    elif request.method == "PUT":
        data = json.loads(request.body)
        user.update({
            "name": data.get("name", user["name"]),
            "last_name": data.get("last_name", user["last_name"]),
            "role": data.get("role", user["role"]),
            "date_of_birth": data.get("date_of_birth", user["date_of_birth"])
        })
        return JsonResponse(user)

    elif request.method == "DELETE":
        users.remove(user)
        return JsonResponse({"message": "User deleted", "id": user["id"]})
