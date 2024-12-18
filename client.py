import tkinter as tk
from tkinter import filedialog, messagebox
from qr_utils import decode_qr
import socket
import json

# Load configuration
with open("config.json") as config_file:
    config = json.load(config_file)

def scan_qr_and_validate():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
    if not file_path:
        return
    try:
        ticket_id = decode_qr(file_path)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((config["server"]["host"], config["server"]["port"]))
        client_socket.send(ticket_id.encode())
        response = client_socket.recv(1024).decode()
        client_socket.close()
        messagebox.showinfo("Validation Result", "Ticket is VALID" if response == "VALID" else "Ticket is INVALID")
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("QR Validation Client")
btn = tk.Button(root, text="Scan and Validate QR Code", command=scan_qr_and_validate)
btn.pack(pady=20)
root.mainloop()
