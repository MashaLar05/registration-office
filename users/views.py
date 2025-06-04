from bson import ObjectId
from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
import bcrypt

from db_connect import users_collection


def index(request):
    user = request.session.get("user")
    return render(request, "index.html", {"user": user})


@csrf_exempt
def all_users(request):
    if request.method == "GET":
        if request.headers.get("Accept") == "application/json":
            users = []
            for user in users_collection.find():
                user["id"] = str(user["_id"])
                del user["_id"]
                if "password" in user:
                    del user["password"]
                users.append(user)
            return JsonResponse(users, safe=False)
        else:
            user = request.session.get("user")
            if not user or user["role"] != "admin":
                return redirect("/login/")
            return render(request, "users_entity.html", {"table_name": "Users"})

    elif request.method == "POST":
        if request.content_type == "application/json":
            data = json.loads(request.body)
        else:
            data = request.POST

        raw_date = data.get("date_of_birth", "")
        try:
            formatted_date = datetime.fromisoformat(raw_date).isoformat()
        except ValueError:
            formatted_date = ""

        role = data.get("role", "")
        if role not in ["user", "admin"]:
            return JsonResponse({"error": "Invalid role. Must be 'user' or 'admin'."}, status=400)

        password = data.get("password")
        if not password:
            return JsonResponse({"error": "Password is required"}, status=400)

        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())

        new_user = users_collection.insert_one({
            "name": data.get("name", ""),
            "last_name": data.get("last_name", ""),
            "role": role,
            "date_of_birth": formatted_date,
            "password": hashed_password.decode('utf-8')
        })
        user = users_collection.find_one({"_id": new_user.inserted_id})
        user["id"] = str(user["_id"])
        del user["_id"]
        del user["password"]
        return JsonResponse(user)


@csrf_exempt
def user_detail(request, user_id):
    try:
        id = ObjectId(user_id)
    except:
        return JsonResponse({"message": "Invalid ID format"}, status=400)

    user = users_collection.find_one({"_id": id})
    if not user:
        return HttpResponseNotFound(json.dumps({"message": "User not found"}), content_type="application/json")

    if request.method == "GET":
        user["id"] = str(user["_id"])
        del user["_id"]
        if "password" in user:
            del user["password"]
        return JsonResponse(user)

    elif request.method == "PUT":
        if request.content_type == "application/json":
            data = json.loads(request.body)
        else:
            data = request.POST

        raw_date = data.get("date_of_birth", "")
        try:
            formatted_date = datetime.fromisoformat(raw_date).isoformat()
        except ValueError:
            formatted_date = user["date_of_birth"]

        role = data.get("role", "")
        if role not in ["user", "admin"]:
            return JsonResponse({"error": "Invalid role. Must be 'user' or 'admin'."}, status=400)

        update_data = {
            "name": data.get("name", user["name"]),
            "last_name": data.get("last_name", user["last_name"]),
            "role": role,
            "date_of_birth": formatted_date
        }

        if data.get("password"):
            update_data["password"] = bcrypt.hashpw(
                data["password"].encode('utf-8'),
                bcrypt.gensalt()
            ).decode('utf-8')

        users_collection.update_one({"_id": id}, {"$set": update_data})
        user = users_collection.find_one({"_id": id})
        user["id"] = str(user["_id"])
        del user["_id"]
        if "password" in user:
            del user["password"]
        return JsonResponse(user)

    elif request.method == "DELETE":
        result = users_collection.delete_one({"_id": id})
        if result.deleted_count == 1:
            return JsonResponse({"message": "User deleted", "id": user_id})
        else:
            return JsonResponse({"message": "User not found"}, status=404)


def index(request):
    user = request.session.get("user")
    if user and user.get("role") in ["admin", "user"]:
        return render(request, "main_auth.html", {"user": user})
    return render(request, "main.html", {})


@csrf_exempt
def register_view(request):
    if request.method == "GET":
        return render(request, "register.html")

    elif request.method == "POST":
        if request.content_type == "application/json":
            data = json.loads(request.body)
        else:
            data = request.POST

        name = data.get("name")
        last_name = data.get("last_name")
        role = data.get("role", "user")
        password = data.get("password")
        raw_date = data.get("date_of_birth", "")

        if not all([name, last_name, password]):
            return JsonResponse({"error": "Name, last name, and password are required"}, status=400)

        if role not in ["user", "admin"]:
            return JsonResponse({"error": "Invalid role. Must be 'user' or 'admin'."}, status=400)

        if users_collection.find_one({"name": name, "last_name": last_name}):
            return JsonResponse({"error": "User already exists"}, status=400)

        try:
            formatted_date = datetime.fromisoformat(raw_date).isoformat()
        except ValueError:
            formatted_date = ""

        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())

        new_user = users_collection.insert_one({
            "name": name,
            "last_name": last_name,
            "role": role,
            "date_of_birth": formatted_date,
            "password": hashed_password.decode('utf-8')
        })

        user = users_collection.find_one({"_id": new_user.inserted_id})
        if not user:
            return JsonResponse({"error": "Failed to retrieve user after registration"}, status=500)

        session_user = {
            "id": str(user["_id"]),
            "name": user.get("name", ""),
            "last_name": user.get("last_name", ""),
            "role": user.get("role", "user")
        }

        request.session["user"] = session_user
        request.session.modified = True
        request.session.save()

        return JsonResponse({"redirect_url": "/"})


@csrf_exempt
def login_view(request):
    if request.method == "GET":
        return render(request, "login.html")

    elif request.method == "POST":
        if request.content_type == "application/json":
            data = json.loads(request.body)
        else:
            data = request.POST

        name = data.get("name")
        password = data.get("password")

        if not all([name, password]):
            return JsonResponse({"error": "Name and password are required"}, status=400)

        user = users_collection.find_one({"name": name})
        if not user:
            return JsonResponse({"error": "Користувача не знайдено"}, status=401)

        if bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
            session_user = {
                "id": str(user["_id"]),
                "name": user.get("name", ""),
                "last_name": user.get("last_name", ""),
                "role": user.get("role", "user")
            }

            request.session["user"] = session_user
            request.session.modified = True
            request.session.save()

            return JsonResponse({"redirect_url": "/"})
        else:
            return JsonResponse({"error": "Невірний пароль"}, status=401)


def logout_view(request):
    request.session.flush()
    return redirect("/")


def user_profile(request, user_id):
    session_user = request.session.get("user")
    if not session_user:
        return redirect("/login/")

    if session_user["role"] == "user" and str(session_user["id"]) != str(user_id):
        return HttpResponseNotFound("Немає доступу")

    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        return HttpResponseNotFound("Користувача не знайдено")

    if request.method == "POST":
        if request.content_type == "application/json":
            data = json.loads(request.body)
        else:
            data = request.POST

        raw_date = data.get("date_of_birth", "")
        try:
            formatted_date = datetime.fromisoformat(raw_date).isoformat()
        except ValueError:
            formatted_date = user["date_of_birth"]

        update_data = {
            "name": data.get("name", user["name"]),
            "last_name": data.get("last_name", user["last_name"]),
            "date_of_birth": formatted_date
        }

        if data.get("password"):
            update_data["password"] = bcrypt.hashpw(
                data["password"].encode('utf-8'),
                bcrypt.gensalt()
            ).decode('utf-8')

        users_collection.update_one(
            {"_id": ObjectId(user_id)}, {"$set": update_data})
        session_user = {
            "id": str(user["_id"]),
            "name": update_data["name"],
            "last_name": update_data["last_name"],
            "role": user["role"]
        }
        request.session["user"] = session_user
        request.session.modified = True
        request.session.save()
        return JsonResponse({"redirect_url": "/"})

    user["id"] = str(user["_id"])
    if "password" in user:
        del user["password"]
    return render(request, "user_page.html", {"user": user})


@csrf_exempt
def create_appointment(request):
    user = request.session.get("user")
    if not user or user["role"] != "user":
        return redirect("/login/")
    return render(request, "create_appointment.html", {"user": user})
