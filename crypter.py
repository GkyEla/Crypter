import os
import random
import string

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def generate_key():
    return os.urandom(32)

def encrypt(payload, key):
    iv = os.urandom(12)
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), default_backend())
    encryptor = cipher.encryptor()
    return encryptor.update(payload) + encryptor.finalize()

def decrypt(payload, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(payload) + decryptor.finalize()

def main():
    payload = open("payload.exe", "rb").read()
    key = generate_key()

    print("Payload will be split into chunks.")
    chunks = split_payload(payload)

    print("Each chunk will be encrypted with a different algorithm.")
    for chunk in chunks:
        try:
            if int(chunk) % 3 == 0:
                chunk_encrypted = encrypt(chunk, key, algorithms.AES(key))
            elif int(chunk) % 3 == 1:
                chunk_encrypted = encrypt(chunk, key, algorithms.ChaCha20Poly1305())
            else:
                chunk_encrypted = encrypt(chunk, key, algorithms.RSA())
        except ValueError:
            # Skip chunks that contain non-digit characters
            continue

    print("Encrypted payload will be saved to a random location.")
    random_dir = os.path.join(os.getcwd(), ''.join(random.choice(string.ascii_lowercase) for _ in range(10)))
    os.makedirs(random_dir, exist_ok=True)
    with open(os.path.join(random_dir, "payload_encrypted.exe"), "wb") as file:
        for chunk_encrypted in chunks:
            file.write(chunk_encrypted)

    print("Process completed.")

def split_payload(payload):
    chunks = [payload[i:i + 1024] for i in range(0, len(payload), 1024)]
    return chunks

if __name__ == "__main__":
    main()
