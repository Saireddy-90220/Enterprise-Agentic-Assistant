import sqlite3
import os
from src.config import DATA_DIR
import json

DB_PATH = os.path.join(DATA_DIR, "enterprise_data.db")

def init_mock_db():
    """Initializes a mock SQLite database with structured enterprise data."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS financials (
        id INTEGER PRIMARY KEY,
        department TEXT,
        q1_revenue INTEGER,
        q2_revenue INTEGER,
        q3_revenue INTEGER,
        q4_revenue INTEGER,
        annual_budget INTEGER
    )
    ''')
    
    # Insert mock data if empty
    cursor.execute('SELECT COUNT(*) FROM financials')
    if cursor.fetchone()[0] == 0:
        data = [
            ('Engineering', 1500000, 1600000, 1750000, 2000000, 8000000),
            ('Sales', 3000000, 3200000, 3500000, 4100000, 12000000),
            ('Marketing', 800000, 850000, 900000, 1100000, 4500000)
        ]
        cursor.executemany('INSERT INTO financials (department, q1_revenue, q2_revenue, q3_revenue, q4_revenue, annual_budget) VALUES (?, ?, ?, ?, ?, ?)', data)
        conn.commit()
    conn.close()

def execute_sql_query(query: str):
    """Executes a SQL query against the enterprise database."""
    if not os.path.exists(DB_PATH):
        init_mock_db()
        
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query)
        columns = [description[0] for description in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()
        return json.dumps(results, indent=2)
    except Exception as e:
        return f"SQL Execution Error: {str(e)}"

# Initialize it proactively
init_mock_db()
