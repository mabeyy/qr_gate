import cv2
import numpy as np
from pyzbar.pyzbar import decode  # Assuming pyzbar is being used for QR code decoding
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

def decode_qr_from_camera(cap, last_scanned_code, last_scanned_time):
    # Capture frame from the already opened camera
    ret, frame = cap.read()
    if not ret:
        logging.error("Error: Failed to capture image.")
        return None

    # Decode the QR codes in the frame
    decoded_objects = decode(frame)
    new_decoded_objects = []

    for obj in decoded_objects:
        ticket_id = obj.data.decode("utf-8")
        current_time = time.time()

        # Check if the same QR code is scanned again within 5 seconds
        if ticket_id != last_scanned_code or (current_time - last_scanned_time) > 5:
            logging.info(f"QR Code Detected: {ticket_id}")

            # Update last scanned code and timestamp
            last_scanned_code = ticket_id
            last_scanned_time = current_time

            # Draw a rectangle around the detected QR code
            rect_points = obj.polygon
            if len(rect_points) == 4:
                pts = [tuple(point) for point in rect_points]
                cv2.polylines(frame, [np.array(pts, dtype=np.int32)], True, (0, 255, 0), 2)
            else:
                cv2.circle(frame, (obj.rect[0], obj.rect[1]), 5, (0, 0, 255), 2)

            new_decoded_objects.append(obj)

    # Display the live camera feed
    cv2.imshow("QR Code Scanner", frame)

    return new_decoded_objects  # Return the decoded objects
