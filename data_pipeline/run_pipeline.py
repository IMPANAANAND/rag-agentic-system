from datetime import datetime
from downloader import download_federal_register_data
from processor import process_data
from db_writer import write_to_db
import json

def run_pipeline():
    end_date = "2024-12-31"
    start_date = "2024-01-01"
    
    try:
        raw_data = download_federal_register_data(start_date, end_date)
    except Exception as e:
        print(f"Error downloading data: {e}")
        return
    
    if not raw_data.get('results'):
        print("No data returned from API.")
        return
    
    raw_file = f"../data/raw/federal_register_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(raw_file, 'w') as f:
        json.dump(raw_data, f)
    processed_file = process_data(raw_file)
    write_to_db(processed_file)

if __name__ == "__main__":
    run_pipeline()