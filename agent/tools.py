import mysql.connector
from typing import List, Dict

def query_mysql_database(query: str, params: tuple = ()) -> List[Dict]:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Impana@2410",  # Replace with your actual password
        database="federal_register_db"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results