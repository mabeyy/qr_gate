import sqlite3
import os

# Define the path for the database
def get_database_path():
    # Get the absolute path of the 'database' folder, relative to the script's location
    return os.path.join(os.path.dirname(__file__), '..', 'database', 'tickets.db')

def setup_database():
    db_path = get_database_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id TEXT PRIMARY KEY,
            id_type TEXT,
            qr_path TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_ticket(ticket_id, id_type, qr_path, status="unused"):
    db_path = get_database_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tickets (ticket_id, id_type, qr_path, status) 
        VALUES (?, ?, ?, ?)
    """, (ticket_id, id_type, qr_path, status))
    conn.commit()
    conn.close()

def validate_ticket(ticket_id):
    db_path = get_database_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM tickets WHERE ticket_id = ?", (ticket_id,))
    result = cursor.fetchone()
    conn.close()
    
    # Check if ticket exists and is unused
    if result is None:
        return False  # Ticket does not exist
    return result[0] == "unused"

def mark_ticket_as_used(ticket_id):
    db_path = get_database_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("UPDATE tickets SET status = 'used' WHERE ticket_id = ?", (ticket_id,))
    conn.commit()
    conn.close()
