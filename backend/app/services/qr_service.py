import cv2
import numpy as np


def scan_qr(file_bytes: bytes) -> str:
    """
    Extract QR data using OpenCV (stable, no external dependencies).
    """

    try:
        # Convert bytes → image
        np_arr = np.frombuffer(file_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if img is None:
            raise ValueError("Invalid image file")

        # Use OpenCV QR detector
        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(img)

        if not data:
            raise ValueError("No QR code detected")

        return data

    except Exception as e:
        raise ValueError(f"QR scanning failed: {str(e)}")