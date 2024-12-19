import sys
import os
import socket
import threading
import logging
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.database import setup_database, validate_ticket, mark_ticket_as_used

config_path = os.path.join(os.path.dirname(__file__), '../config.json')

# Load configuration
with open(config_path) as config_file:
    config = json.load(config_file)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def handle_client(client_socket):
    try:
        ticket_id = client_socket.recv(1024).decode()
        logging.info(f"Received Ticket ID: {ticket_id}")

        if validate_ticket(ticket_id):
            client_socket.send("VALID".encode())
            mark_ticket_as_used(ticket_id)  # Mark ticket as used
            logging.info(f"Ticket {ticket_id} marked as used.")
        else:
            client_socket.send("INVALID".encode())
            logging.info(f"Ticket {ticket_id} is invalid or already used.")
    except Exception as e:
        logging.error(f"Error: {e}")
    finally:
        client_socket.close()

def start_server():
    setup_database()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((config["server"]["host"], config["server"]["port"]))
    server_socket.listen(5)
    logging.info("Server is running...")
    while True:
        client_socket, _ = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()
