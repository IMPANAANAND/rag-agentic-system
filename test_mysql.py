import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Replace with your password
    database="federal_register_db"
)
print("Connected successfully!")
conn.close()
