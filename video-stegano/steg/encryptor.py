from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

def generate_key(algorithm):
    if algorithm == "AES":
        key = get_random_bytes(16)
        return key, key.hex()
    elif algorithm == "RSA":
        key = RSA.generate(2048)
        return key, key.export_key().decode()
    elif algorithm == "Kyber":
        key = get_random_bytes(32)
        return key, key.hex()

def encrypt_message(message, key, algorithm):
    if algorithm == "AES":
        cipher = AES.new(key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(message.encode())
        return cipher.nonce + tag + ciphertext
    elif algorithm == "RSA":
        cipher = PKCS1_OAEP.new(key.publickey())
        return cipher.encrypt(message.encode())
    elif algorithm == "Kyber":
        return bytes([b ^ key[i % len(key)] for i, b in enumerate(message.encode())])

def decrypt_message(ciphertext, key, algorithm):
    if algorithm == "AES":
        nonce = ciphertext[:16]
        tag = ciphertext[16:32]
        ct = ciphertext[32:]
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        return cipher.decrypt_and_verify(ct, tag).decode()
    elif algorithm == "RSA":
        cipher = PKCS1_OAEP.new(key)
        return cipher.decrypt(ciphertext).decode()
    elif algorithm == "Kyber":
        return bytes([b ^ key[i % len(key)] for i, b in enumerate(ciphertext)]).decode()
