import sqlite3
from tabulate import tabulate

def fetch_analysis(limit=None, last_only=False, all_entries=False):
    conn = sqlite3.connect('blood_analysis.db')
    cursor = conn.cursor()

    if last_only:
        cursor.execute('''
            SELECT a.id, a.file_id, f.filename, a.query, a.output, a.status, a.analyzed_at
            FROM analysis a
            JOIN files f ON a.file_id = f.id
            ORDER BY a.analyzed_at DESC
            LIMIT 1
        ''')
    elif all_entries:
        cursor.execute('''
            SELECT a.id, a.file_id, f.filename, a.query, a.output, a.status, a.analyzed_at
            FROM analysis a
            JOIN files f ON a.file_id = f.id
            ORDER BY a.analyzed_at DESC
        ''')
    elif limit:
        cursor.execute('''
            SELECT a.id, a.file_id, f.filename, a.query, a.output, a.status, a.analyzed_at
            FROM analysis a
            JOIN files f ON a.file_id = f.id
            ORDER BY a.analyzed_at DESC
            LIMIT ?
        ''', (limit,))
    else:
        print("Invalid option.")
        return []

    rows = cursor.fetchall()
    conn.close()
    return rows

def display_table(rows):
    headers = ["Analysis ID", "File ID", "Filename", "Query", "Output", "Status", "Analyzed At"]
    print(tabulate(rows, headers=headers, tablefmt="grid", maxcolwidths=[None, None, 20, 20, 20, None, None]))

def main():
    print("Database Viewer for blood_analysis.db")
    while True:
        print("\nOptions:")
        print("1. Show all entries")
        print("2. Show last entry")
        print("3. Show last N entries")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            rows = fetch_analysis(all_entries=True)
            display_table(rows)
        elif choice == "2":
            rows = fetch_analysis(last_only=True)
            display_table(rows)
        elif choice == "3":
            n = int(input("Enter N: "))
            rows = fetch_analysis(limit=n)
            display_table(rows)
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
