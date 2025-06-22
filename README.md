# 🎥🔐 Video Steganography Web App

A Python + Streamlit-based web application that hides and retrieves **text or image data** inside **MP4 video files** using multiple encryption algorithms: **AES**, **RSA**, and **Kyber** (Post-Quantum). The app also displays **time frame info**, **encryption status**, and calculates **PSNR** metrics.

---

## 🧠 Features

- 🔐 **Supports AES, RSA, and Kyber encryption**
- 🖼️ Hide both **text and images** in videos
- 🎞️ Displays **frame position** for embedded/extracted data
- 📈 Shows **PSNR (Peak Signal-to-Noise Ratio)** to measure video quality
- 📁 Upload and download processed video files
- 🧮 User-friendly **Streamlit interface** with interactive options
- 💡 Real-time encoding/decoding logs
- ✅ Supports download of encoded video and decrypted messages

---

## 🧰 Tech Stack

- **Frontend/UI**: Streamlit
- **Backend**: Python
- **Encryption**: AES, RSA, Kyber
- **Libraries**: OpenCV, PyCryptodome, NumPy, Scikit-image, etc.

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/video-steganography-streamlit.git
cd video-steganography-streamlit
