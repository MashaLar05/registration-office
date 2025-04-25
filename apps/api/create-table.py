import psycopg2

conn = psycopg2.connect(dbname = "registrationoffice", user="postgres", password="12345", host="localhost", port="5432")
cursor = conn.cursor()

cursor.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, name VARCHAR(50), last_name VARCHAR(50), role VARCHAR(50), date_of_birth DATE)")
cursor.execute("CREATE TABLE doctors (id SERIAL PRIMARY KEY, name VARCHAR(50), last_name VARCHAR(50), qualification VARCHAR(50), date_of_birth DATE)")
cursor.execute("CREATE TABLE appointments (id SERIAL PRIMARY KEY, date_time DATE, user_id INTEGER, doctor_id INTEGER)")

conn.commit()

cursor.close()
conn.close()