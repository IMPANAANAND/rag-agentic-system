# RAG Agentic System for Federal Register Executive Orders

A Retrieval-Augmented Generation (RAG) system that fetches U.S. executive orders from the Federal Register API, stores them in a MySQL database, and allows users to query them via a FastAPI server and Streamlit UI. Leveraging Ollama’s Qwen2.5 model, the system summarizes query results, providing an intuitive interface to explore executive orders.

---

## Features

* **Data Pipeline:** Downloads executive orders from the Federal Register API and stores them in a MySQL database.
* **FastAPI Server:** Provides an API endpoint to query executive orders with LLM-powered summarization.
* **Streamlit UI:** User-friendly web interface to submit queries and view summarized results.
* **Ollama Integration:** Uses the Qwen2.5:0.5b model for natural language summarization.
* **MySQL Database:** Stores executive order data including document number, title, publication date, president, abstract, and URL.

---

## Prerequisites

* **Operating System:** Windows 10/11 (tested)
* **Python:** 3.8 or higher
* **MySQL:** 8.0 or higher
* **Ollama:** Latest version with Qwen2.5:0.5b model
* **Git:** For cloning the repository
* **PowerShell:** For running commands
* **Internet Connection:** Required for API calls and dependencies

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/rag-agentic-system.git
cd rag-agentic-system
```

### 2. Set Up Virtual Environment

```bash
python -m venv env
.\env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install and Configure MySQL

* Download and install MySQL 8.0 from [mysql.com](https://www.mysql.com/).
* Set up a root user with a secure password (replace `mysecret123` with your password in code).
* Create the database and tables by running:

```powershell
Get-Content db\schema.sql | mysql -u root -p
```

### 5. Install Ollama and Qwen2.5 Model

* Download Ollama from [ollama.com](https://ollama.com/).
* Install and pull the model:

```bash
ollama pull qwen2.5:0.5b
```

### 6. Update Configuration

Update MySQL credentials in the following files, replacing `mysecret123` with your password:

* `data_pipeline/db_writer.py`
* `agent/tools.py`
* `test_mysql.py`

Example MySQL connection snippet:

```python
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="federal_register_db"
)
```

---

## Usage

### 1. Run the Data Pipeline

Fetch executive orders and store them in MySQL:

```bash
python data_pipeline\run_pipeline.py
```

* Outputs JSON files to `data/raw/`
* Outputs CSV files to `data/processed/`
* Populates the `executive_orders` table in `federal_register_db`

### 2. Run the FastAPI Server

* Start Ollama server:

```bash
ollama serve
```

* Run FastAPI:

```bash
python api\main.py
```

* Test API with curl:

```bash
curl -X POST "http://localhost:8000/query" -H "Content-Type: application/json" -d "{\"query\":\"What are the new executive orders in 2024?\"}"
```

### 3. Run the Streamlit UI

```bash
streamlit run ui\app.py
```

* Open [http://localhost:8501](http://localhost:8501) in your browser
* Enter queries like “What are the new executive orders in 2024?” and view summarized results

---

## Project Structure

```
rag-agentic-system/
├── api/
│   └── main.py               # FastAPI server
├── agent/
│   ├── __init__.py           # Package marker
│   ├── agent.py              # Ollama query processing
│   └── tools.py              # MySQL query utility
├── data_pipeline/
│   ├── downloader.py         # Federal Register API fetcher
│   ├── processor.py          # JSON to CSV processing
│   ├── db_writer.py          # CSV to MySQL writer
│   └── run_pipeline.py       # Pipeline orchestrator
├── db/
│   └── schema.sql            # MySQL database schema
├── data/
│   ├── raw/                  # Raw JSON data
│   └── processed/            # Processed CSV files
├── ui/
│   └── app.py                # Streamlit UI
├── requirements.txt          # Python dependencies
├── test_mysql.py             # MySQL connection test script
└── README.md                 # This file
```

---

## Troubleshooting

* **Ollama Port Conflict (11434):**

  Check process:

  ```powershell
  netstat -ano | findstr 11434
  ```

  Kill conflicting process:

  ```powershell
  taskkill /PID <pid> /F
  ```

* **FastAPI Silent Failure:**

  * Enable debug logging in `api/main.py`.
  * Verify `agent/agent.py` and `agent/tools.py`.

* **Streamlit Connection Error:**

  * Confirm FastAPI is running on port 8000:

  ```powershell
  netstat -ano | findstr 8000
  ```

  * Add firewall rule to allow port 8000:

  ```powershell
  netsh advfirewall firewall add rule name="Allow Port 8000" dir=in action=allow protocol=TCP localport=8000
  ```

* **Database Issues:**

  Verify number of rows:

  ```mysql
  USE federal_register_db;
  SELECT COUNT(*) FROM executive_orders;
  ```

  Rerun pipeline if needed:

  ```bash
  python data_pipeline\run_pipeline.py
  ```

---

## Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m "Add feature"`
4. Push to the branch: `git push origin feature-name`
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
