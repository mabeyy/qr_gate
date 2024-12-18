import qrcode
import os
import sqlite3

def generate_qr(ticket_id, save_dir="qr"):
    import os
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    qr = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(ticket_id)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img_path = os.path.join(save_dir, f"{ticket_id}.png")
    img.save(img_path)
    return img_path

def add_ticket_to_db_with_path(ticket_id, id_type, qr_path, status="unused"):
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
    
    # Ensure the table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id TEXT PRIMARY KEY,
            id_type TEXT,
            qr_path TEXT,
            status TEXT
        )
    """)
    
    # Check if the ticket already exists
    cursor.execute("SELECT ticket_id FROM tickets WHERE ticket_id = ?", (ticket_id,))
    existing_ticket = cursor.fetchone()
    
    if existing_ticket:
        print(f"Ticket with ID {ticket_id} already exists. Skipping insert.")
    else:
        # Insert ticket data with QR code path
        cursor.execute("INSERT INTO tickets (ticket_id, id_type, qr_path, status) VALUES (?, ?, ?, ?)", 
                       (ticket_id, id_type, qr_path, status))
        conn.commit()
        print(f"Ticket {ticket_id} with QR saved at {qr_path} added to database.")
    
    conn.close()

def create_ticket(ticket_id, id_type, status):
    # Generate QR code and get its path
    qr_path = generate_qr(ticket_id)
    
    # Add ticket to the database
    add_ticket_to_db_with_path(ticket_id, id_type, qr_path, status)

def delete_ticket(ticket_id):
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()

    # Check if the ticket exists in the database
    cursor.execute("SELECT qr_path FROM tickets WHERE ticket_id = ?", (ticket_id,))
    existing_ticket = cursor.fetchone()

    if existing_ticket:
        # Extract the QR code path from the database
        qr_path = existing_ticket[0]

        # Delete the ticket from the database
        cursor.execute("DELETE FROM tickets WHERE ticket_id = ?", (ticket_id,))
        conn.commit()
        print(f"Ticket {ticket_id} deleted from the database.")
        
        # Delete the QR code image file
        if os.path.exists(qr_path):
            os.remove(qr_path)
            print(f"QR code image for ticket {ticket_id} deleted from file system.")
        else:
            print(f"QR code image for ticket {ticket_id} not found.")
    else:
        print(f"Ticket with ID {ticket_id} does not exist.")

    conn.close()

while True:
    print("\n1. Add ticket \n2. Delete a ticket \n3. Exit")
    inp = input("Select a number: ")
    
    if inp == "1":
        ticket_id = input("\nEnter ticket ID: ")
        id_type = input("Enter ID type (Regular, Special): ")
        create_ticket(ticket_id, id_type, status='unused')
    elif inp == "2":
        ticket_id = input("\nEnter ticket ID to delete: ")
        delete_ticket(ticket_id)
    elif inp == "3":
        break
    else:
        print('\nInvalid input. Enter number a 1-3.')
