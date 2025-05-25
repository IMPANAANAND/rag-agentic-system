import mysql.connector
import csv

def write_to_db(csv_file: str) -> None:
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Impana@2410",  # Replace with your actual password
            database="federal_register_db"
        )
        cursor = conn.cursor()
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                query = """
                INSERT INTO executive_orders (document_number, title, publication_date, president, abstract, full_text_url)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                values = (
                    row['document_number'],
                    row['title'],
                    row['publication_date'] or None,
                    row['president'],
                    row['abstract'],
                    row['full_text_url']
                )
                try:
                    cursor.execute(query, values)
                    print(f"Inserted row: {row['document_number']}")
                except mysql.connector.Error as e:
                    print(f"Error inserting row {row['document_number']}: {e}")
                    continue
        
        conn.commit()
        print(f"Total rows inserted: {cursor.rowcount}")
    except mysql.connector.Error as e:
        print(f"MySQL Error: {e}")
    finally:
        cursor.close()
        conn.close()