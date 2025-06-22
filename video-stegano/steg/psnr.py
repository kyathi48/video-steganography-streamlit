import cv2
import numpy as np
from skimage.metrics import peak_signal_noise_ratio as psnr

def calculate_psnr(original_path, encoded_path):
    cap_orig = cv2.VideoCapture(original_path)
    cap_encoded = cv2.VideoCapture(encoded_path)

    psnr_total = 0
    count = 0

    while True:
        ret1, frame1 = cap_orig.read()
        ret2, frame2 = cap_encoded.read()

        if not ret1 or not ret2:
            break

        value = psnr(frame1, frame2)
        psnr_total += value
        count += 1

    cap_orig.release()
    cap_encoded.release()

    return round(psnr_total / count, 2) if count else 0
