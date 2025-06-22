import streamlit as st
import os
from steg.encoder import encode_video
from steg.decoder import decode_video
from steg.encryptor import generate_key, encrypt_message, decrypt_message

st.set_page_config(page_title="Video Steganography", layout="centered")
st.title("🎥 Video Steganography with Encryption")

tabs = st.tabs(["🔐 Encode", "🔓 Decode"])

with tabs[0]:
    st.header("Encode Message into Video")

    video_file = st.file_uploader("Upload Video", type=["mp4"], key="encode_video")
    message = st.text_area("Message to Encode")

    encryption_algo = st.selectbox("Select Encryption Algorithm", ["AES", "RSA", "Kyber"])

    if video_file and message:
        if st.button("Encode Video"):
            with st.spinner("Encoding..."):

                # Save video locally
                input_path = os.path.join("temp", video_file.name)
                os.makedirs("temp", exist_ok=True)
                with open(input_path, "wb") as f:
                    f.write(video_file.read())

                # Generate encryption key
                key_info, key_display = generate_key(encryption_algo)

                # Encrypt the message
                encrypted_msg = encrypt_message(message, key_info, encryption_algo)

                # Encode the video
                output_path, frame_info, psnr_value = encode_video(input_path, encrypted_msg)

                st.success("Video encoded successfully! ✅")

                # Show frame and PSNR
                st.markdown(f"**Embedded at frame**: {frame_info}")
                st.markdown(f"**PSNR value**: `{psnr_value:.2f}` dB")

                # Download encoded video
                with open(output_path, "rb") as f:
                    st.download_button("📥 Download Encoded Video", f, file_name="encoded_video.mp4")

                # Show & download encryption key
                st.markdown("### 🔑 Encryption Key")
                st.code(key_display, language="text")
                st.download_button("📥 Download Key", key_display, file_name="encryption_key.txt")

with tabs[1]:
    st.header("Decode Message from Video")

    decode_video_file = st.file_uploader("Upload Encoded Video", type=["mp4"], key="decode_video")
    decode_key = st.text_area("Paste Decryption Key")

    selected_algo = st.selectbox("Select Encryption Algorithm Used", ["AES", "RSA", "Kyber"], key="decode_algo")

    if decode_video_file and decode_key:
        if st.button("Decode Video"):
            with st.spinner("Decoding..."):

                # Save uploaded video
                decode_input_path = os.path.join("temp", "uploaded_encoded.mp4")
                with open(decode_input_path, "wb") as f:
                    f.write(decode_video_file.read())

                # Reconstruct key
                if selected_algo == "AES":
                    key = bytes.fromhex(decode_key)
                elif selected_algo == "RSA":
                    from Crypto.PublicKey import RSA
                    key = RSA.import_key(decode_key)
                elif selected_algo == "Kyber":
                    key = bytes.fromhex(decode_key)

                # Decode and decrypt
                encoded_msg, frame_info = decode_video(decode_input_path)
                decrypted_msg = decrypt_message(encoded_msg, key, selected_algo)

                # Display result
                st.markdown(f"**Message Found at Frame**: {frame_info}")
                st.markdown("### 📩 Decrypted Message")
                st.success(decrypted_msg)

