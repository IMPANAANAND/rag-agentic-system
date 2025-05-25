import json
import csv
import os
from datetime import datetime

def process_data(raw_file: str) -> str:
    with open(raw_file, 'r') as f:
        data = json.load(f)
    
    documents = data.get('results', [])
    processed_data = []
    
    for doc in documents:
        publication_year = doc.get('publication_date', '')[:4]
        president = "Unknown"
        if publication_year == "2024":
            president = "Joe Biden"
        elif publication_year >= "2025":
            president = "Donald Trump"
        
        processed_data.append({
            'document_number': doc.get('document_number', ''),
            'title': doc.get('title', ''),
            'publication_date': doc.get('publication_date', ''),
            'president': president,
            'abstract': doc.get('abstract', '') or '',
            'full_text_url': doc.get('html_url', '')
        })
    
    os.makedirs("../data/processed", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    processed_file = f"../data/processed/federal_register_{timestamp}.csv"
    with open(processed_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['document_number', 'title', 'publication_date', 'president', 'abstract', 'full_text_url'])
        writer.writeheader()
        writer.writerows(processed_data)
    
    return processed_file