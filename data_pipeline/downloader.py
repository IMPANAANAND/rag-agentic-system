import requests
import json
from datetime import datetime
import os

def download_federal_register_data(start_date: str, end_date: str) -> dict:
    base_url = "https://www.federalregister.gov/api/v1/documents.json"
    params = {
        "conditions[type]": "PRESDOCU",
        "conditions[presidential_document_type]": "executive_order",
        "per_page": 100,
        "order": "newest"
    }
    if start_date and end_date:
        params["conditions[publication_date][gte]"] = start_date
        params["conditions[publication_date][lte]"] = end_date
    
    try:
        response = requests.get(base_url, params=params)
        print(f"API URL: {response.url}")
        print(f"Response: {response.text}")
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        return {}
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return {}
    
    os.makedirs("../data/raw", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    raw_file = f"../data/raw/federal_register_{timestamp}.json"
    with open(raw_file, 'w') as f:
        json.dump(data, f)
    
    return data

if __name__ == "__main__":
    end_date = "2024-12-31"
    start_date = "2024-01-01"
    download_federal_register_data(start_date, end_date)