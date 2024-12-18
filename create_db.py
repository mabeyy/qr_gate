import sqlite3

conn = sqlite3.connect('tickets.db')
cursor = conn.cursor()

# Create table
cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id TEXT PRIMARY KEY,
            id_type TEXT,
            qr_path TEXT
        )
    """)

# cursor.execute("INSERT INTO tickets (ticket_id, id_type, qr_path) VALUES ('01', 'vip', 'qr/01.png')")

# Insert sample data
conn.commit()
conn.close()
