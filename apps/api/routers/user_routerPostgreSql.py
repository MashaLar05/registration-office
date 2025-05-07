from fastapi import APIRouter, Body
import psycopg2
from datetime import datetime
from ..create_table import create_tables_if_not_exists

create_tables_if_not_exists()
conn = psycopg2.connect(dbname="registrationoffice", user="postgres",
                        password="12345", host="localhost", port="5432")

if conn:
    print("Connection is succesfully!")

cursor = conn.cursor()

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/")
def create_user_endpoint(data=Body()):
    db_user = (data["name"], data["last_name"],
               data["role"], data["date_of_birth"])
    try:
        cursor.execute(
            "INSERT INTO users (name, last_name, role, date_of_birth) VALUES (%s, %s, %s, %s)", db_user)
        conn.commit()
        cursor.execute(
            "SELECT id, name, last_name, role, date_of_birth FROM users ORDER BY id DESC LIMIT 1")
        user = cursor.fetchone()
        return {
            "id": user[0],
            "name": user[1],
            "last_name": user[2],
            "role": user[3],
            "date_of_birth": user[4].isoformat()
        }
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}


@router.get("/")
def get_user_endpoint():
    try:
        cursor.execute("SELECT * FROM users")
        return [
            {
                "name": user[1],
                "last_name": user[2],
                "role": user[3],
                "date_of_birth": user[4].isoformat()
            }
            for user in cursor
        ]
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}


@router.get("/{user_id}")
def get_user_by_id_endpoint(user_id: int):
    if user_id is None or user_id <= 0:
        return {"error": "Invalid user_id provided"}
    try:
        cursor.execute(
            "SELECT id, name, last_name, date_of_birth FROM users WHERE id=%s", (user_id,))
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
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}


@router.put("/{user_id}")
def update_user_endpoint(user_id: int, data=Body()):
    data["date_of_birth"] = datetime.fromisoformat(data["date_of_birth"])
    try:
        cursor.execute("UPDATE users SET name = %s, last_name = %s, role = %s, date_of_birth = %s WHERE id = %s",
                       (data["name"], data["last_name"], data["role"], data["date_of_birth"], user_id,))
        conn.commit()
        cursor.execute(
            "SELECT id, name, last_name, role, date_of_birth FROM users WHERE id=%s", (user_id,))
        user = cursor.fetchone()
        conn.commit()
        return {
            "id": user[0],
            "name": user[1],
            "last_name": user[2],
            "role": user[3],
            "date_of_birth": user[4].isoformat()
        }
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}


@router.delete("/{user_id}")
def delete_user_endpoint(user_id: int):
    try:
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}
