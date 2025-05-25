import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Impana@2410",  # Replace with your password
    database="federal_register_db"
)
print("Connected successfully!")
conn.close()