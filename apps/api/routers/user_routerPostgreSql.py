from fastapi import APIRouter, Body
import psycopg2
from datetime import datetime

conn = psycopg2.connect(dbname = "registrationoffice", user = "postgres", password = "12345", host="localhost", port="5432")
cursor = conn.cursor()

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/")
def create_user_endpoint (data = Body()):
    db_user = (data["name"], data["last_name"], data["role"], data["date_of_birth"])
    cursor.execute("INSERT INTO users (name, last_name, role, date_of_birth) VALUES (%s, %s, %s, %s)", db_user)
    conn.commit()
    cursor.execute("SELECT id, name, last_name, role, date_of_birth FROM users ORDER BY id DESC LIMIT 1")
    user = cursor.fetchone()
    return {
            "id": user[0],
            "name": user[1],
            "last_name": user[2],
            "role": user[3],
            "date_of_birth": user[4].isoformat()
         }

@router.get("/")
def get_user_endpoint():
    cursor.execute("SELECT * FROM users")
    return[
        {
            "name": user[1],
            "last_name": user[2],
            "role": user[3],
            "date_of_birth": user[4].isoformat()
        }
        for user in cursor
    ]

@router.get("/{user_id}")
def get_user_by_id_endpoint(user_id: int):
    cursor.execute("SELECT id, name, last_name, date_of_birth FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    if user:
        return {
            "id": user[0],
            "name": user[1],
            "last_name": user[2],
            "date_of_birth": user[3].isoformat()
        }
    else:
        return {"message": "User not found"}

@router.put("/{user_id}")
def update_user_endpoint(user_id: int, data = Body()):
    data["date_of_birth"] = datetime.fromisoformat(data["date_of_birth"])
    cursor.execute("UPDATE users SET name = %s, last_name = %s, role = %s, date_of_birth = %s WHERE id = %s", 
                   (data["name"], data["last_name"], data["role"], data["date_of_birth"], user_id,))
    conn.commit()
    cursor.execute("SELECT id, name, last_name, role, date_of_birth FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    return {
            "name": user[1],
            "last_name": user[2],
            "role": user[3],
            "date_of_birth": user[4].isoformat()
        }

@router.delete("/{user_id}")
def delete_user_endpoint(user_id: int):
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
