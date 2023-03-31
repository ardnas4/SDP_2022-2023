from cryptography.fernet import Fernet as fer
key = fer.generate_key()
with open("keyFile.txt", "wb") as f:
    f.write(key)
# with open("keyFileMatt.txt", "w") as f:
#     # The same
#     f.write(key.decode())
