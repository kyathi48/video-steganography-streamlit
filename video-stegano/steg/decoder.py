import cv2
import numpy as np

def binary_to_text(binary_str):
    chars = [binary_str[i:i+8] for i in range(0, len(binary_str), 8)]
    message = ''.join([chr(int(c, 2)) for c in chars])
    return message.split("#####")[0]

def decode_video(video_path):
    cap = cv2.VideoCapture(video_path)
    binary_data = []
    found_end = False
    frame_num = 0
    end_marker = "#####"
    end_bin = ''.join(format(ord(c), '08b') for c in end_marker)
    buffer_check = ""

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_num += 1

        # Extract LSBs from blue channel
        blue_channel = frame[:, :, 0]
        bits = (blue_channel & 1).flatten()

        for bit in bits:
            binary_data.append(str(bit))
            buffer_check += str(bit)
            # Keep buffer limited to length of end marker binary
            if len(buffer_check) > len(end_bin):
                buffer_check = buffer_check[1:]
            if buffer_check == end_bin:
                found_end = True
                break
        if found_end:
            break

    cap.release()
    binary_str = ''.join(binary_data)
    hidden_msg = binary_to_text(binary_str)
    return hidden_msg, frame_num
