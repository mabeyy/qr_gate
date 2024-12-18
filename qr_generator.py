import qrcode
import os
import sqlite3

def generate_qr(ticket_id):
    # Define directory for saving QR codes
    save_dir = "qr"
    
    # Create the directory if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # Create QR code
    qr = qrcode.QRCode(
        version=2, 
        error_correction=qrcode.constants.ERROR_CORRECT_L, 
        box_size=10, 
        border=4
    )
    qr.add_data(ticket_id)
    qr.make(fit=True)
    
    # Save QR code image
    img = qr.make_image(fill_color="black", back_color="white")
    img_path = os.path.join(save_dir, f"{ticket_id}.png")
    img.save(img_path)
    print(f"QR Code for Ticket ID {ticket_id} saved in {save_dir}/")
    return img_path  # Return the path of the saved QR code

def add_ticket_to_db_with_path(ticket_id, id_type, qr_path):
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
    
    # Ensure the table exists (optional, for safety)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id TEXT PRIMARY KEY,
            id_type TEXT,
            qr_path TEXT
        )
    """)
    
    # Insert ticket data with QR code path
    cursor.execute("INSERT INTO tickets (ticket_id, id_type, qr_path) VALUES (?, ?, ?)", 
                   (ticket_id, id_type, qr_path))
    conn.commit()
    conn.close()
    print(f"Ticket {ticket_id} with QR saved at {qr_path} added to database.")

def create_ticket(ticket_id, id_type):
    # Generate QR code and get its path
    qr_path = generate_qr(ticket_id)
    
    # Add ticket to the database
    add_ticket_to_db_with_path(ticket_id, id_type, qr_path)

# User input for ticket creation
ticket_id = input("Enter Ticket ID: ")
id_type = input("Enter ID Type (a, s): ")
create_ticket(ticket_id, id_type)
