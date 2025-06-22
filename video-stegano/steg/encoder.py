def encode_video(input_path, encrypted_bytes):
    import cv2
    import numpy as np
    import os
    from skimage.metrics import peak_signal_noise_ratio as psnr

    def bytes_to_binary(byte_data):
        return ''.join(f'{byte:08b}' for byte in byte_data)

    cap = cv2.VideoCapture(input_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)
    width, height = int(cap.get(3)), int(cap.get(4))

    os.makedirs("output", exist_ok=True)
    output_path = os.path.join("output", "encoded_video.mp4")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Add end marker for decoding
    secret_binary = bytes_to_binary(encrypted_bytes + b'#####')
    bit_index = 0
    embed_frame = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if bit_index < len(secret_binary):
            flat_frame = frame.reshape(-1, 3)  # Reshape for fast access
            for pixel in flat_frame:
                for i in range(3):
                    if bit_index >= len(secret_binary):
                        break
                    pixel[i] = (pixel[i] & ~1) | int(secret_binary[bit_index])
                    bit_index += 1
                if bit_index >= len(secret_binary):
                    break
            frame = flat_frame.reshape(frame.shape)
            if embed_frame is None:
                embed_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

        out.write(frame)

    cap.release()
    out.release()

    # PSNR comparison for quality
    orig = cv2.VideoCapture(input_path)
    enc = cv2.VideoCapture(output_path)
    _, f1 = orig.read()
    _, f2 = enc.read()
    orig.release()
    enc.release()
    psnr_value = psnr(f1, f2)

    return output_path, embed_frame, psnr_value
