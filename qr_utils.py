import qrcode
from pyzbar.pyzbar import decode
from PIL import Image

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

def decode_qr(file_path):
    img = Image.open(file_path)
    qr_data = decode(img)
    if not qr_data:
        raise ValueError("No QR code found!")
    return qr_data[0].data.decode('utf-8')
