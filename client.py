import tkinter as tk
from tkinter import messagebox
from qr_utils import decode_qr_from_camera
import socket
import threading
import json
import cv2
import time
import logging

# Load configuration
with open("config.json") as config_file:
    config = json.load(config_file)

# Setup logging
logging.basicConfig(level=logging.INFO)

def validate_ticket(ticket_id):
    try:
        # Connect to the server to validate the ticket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((config["server"]["host"], config["server"]["port"]))
            client_socket.send(ticket_id.encode())
            response = client_socket.recv(1024).decode()

        # Print result to console
        if response == "VALID":
            logging.info(f"Ticket {ticket_id} is VALID")
        else:
            logging.info(f"Ticket {ticket_id} is INVALID")
    except Exception as e:
        logging.error(f"Error during ticket validation: {str(e)}")

def scan_qr_and_validate():
    # Initialize the camera once
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        logging.error("Error: Could not open camera.")
        return

    try:
        # Variables to manage last scanned QR code and timestamp
        last_scanned_code, last_scanned_time = None, 0

        while True:
            decoded_objects = decode_qr_from_camera(cap, last_scanned_code, last_scanned_time)
            if decoded_objects:
                for obj in decoded_objects:
                    ticket_id = obj.data.decode("utf-8")
                    current_time = time.time()

                    # Check if the same QR code is scanned again within 5 seconds
                    if ticket_id != last_scanned_code or (current_time - last_scanned_time) > 5:
                        # Validate the ticket in a separate thread to avoid blocking the camera feed
                        threading.Thread(target=validate_ticket, args=(ticket_id,)).start()

                        # Update last scanned code and timestamp
                        last_scanned_code = ticket_id
                        last_scanned_time = current_time

                        logging.info(f"Scanned ticket: {ticket_id}")

            # Check for the 'q' key press to break the loop and stop the camera feed
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):  # If 'q' is pressed, stop the loop
                break
    except Exception as e:
        logging.error(f"Error during QR scanning: {str(e)}")
    finally:
        # Release the camera and close all OpenCV windows when done
        cap.release()
        cv2.destroyAllWindows()

# Setup Tkinter window
def create_ui():
    root = tk.Tk()
    root.title("QR Validation Client")
    btn = tk.Button(root, text="Scan and Validate QR Code", command=scan_qr_and_validate)
    btn.pack(pady=20)
    root.mainloop()

if __name__ == "__main__":
    create_ui()
