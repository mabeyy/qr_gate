import sqlite3

def setup_database():
    conn = sqlite3.connect('tickets.db')
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
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tickets (ticket_id, id_type, qr_path, status) 
        VALUES (?, ?, ?, ?, ?)
    """, (ticket_id, id_type, qr_path, status))
    conn.commit()
    conn.close()

def validate_ticket(ticket_id):
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM tickets WHERE ticket_id = ?", (ticket_id,))
    result = cursor.fetchone()
    conn.close()
    
    # Check if ticket exists and is unused
    if result is None:
        return False  # Ticket does not exist
    return result[0] == "unused"

def mark_ticket_as_used(ticket_id):
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE tickets SET status = 'used' WHERE ticket_id = ?", (ticket_id,))
    conn.commit()
    conn.close()
