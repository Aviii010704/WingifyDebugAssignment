# database.py

import sqlite3
import os
import uuid

def init_db():
    """Initialize the database and create tables if they don't exist."""
    conn = sqlite3.connect('blood_analysis.db')
    cursor = conn.cursor()
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS files (
            id TEXT PRIMARY KEY,
            filename TEXT,
            stored_path TEXT,
            size INTEGER,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS analysis (
            id TEXT PRIMARY KEY,
            file_id TEXT,
            query TEXT,
            output TEXT,
            status TEXT,
            analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (file_id) REFERENCES files(id)
        );
    ''')
    conn.commit()
    conn.close()

def save_file_and_analysis(filename, stored_path, size, query, output, status):
    """
    Save file and analysis data to the database.
    """
    conn = sqlite3.connect('blood_analysis.db')
    cursor = conn.cursor()
    file_id = str(uuid.uuid4())
    analysis_id = str(uuid.uuid4())
    cursor.execute(
        'INSERT INTO files (id, filename, stored_path, size) VALUES (?, ?, ?, ?)',
        (file_id, filename, stored_path, size)
    )
    cursor.execute(
        'INSERT INTO analysis (id, file_id, query, output, status) VALUES (?, ?, ?, ?, ?)',
        (analysis_id, file_id, query, output, status)
    )
    conn.commit()
    conn.close()
    update_csv_export()
    
import csv

def update_csv_export():
    """Export all analysis data to a CSV file."""
    conn = sqlite3.connect('blood_analysis.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT a.id, a.file_id, f.filename, a.query, a.output, a.status, a.analyzed_at
        FROM analysis a
        JOIN files f ON a.file_id = f.id
    ''')
    rows = cursor.fetchall()
    conn.close()

    csv_path = 'analysis_data.csv'
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Analysis ID', 'File ID', 'Filename', 'Query', 'Output', 'Status', 'Analyzed At'])
        writer.writerows(rows)
