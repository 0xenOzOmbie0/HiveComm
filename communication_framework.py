from cryptography.fernet import Fernet
import hashlib

class KeyManagementService:
    def __init__(self):
        self.key = Fernet.generate_key()

    def get_key(self):
        return self.key

class Message:
    def __init__(self, header, body, footer, metadata=None, kms=None):
        self.header = header
        self.body = body
        self.footer = footer
        self.metadata = metadata if metadata else {}
        self.kms = kms  # Key Management Service

    def encode(self):
        key = self.kms.get_key()  # Get the existing key
        f = Fernet(key)
        encrypted_message = f.encrypt(self.body.encode())
        checksum = hashlib.md5(self.body.encode()).hexdigest()
        return encrypted_message, checksum

    def decode(self, encrypted_message, checksum):
        key = self.kms.get_key()  # Get the key
        f = Fernet(key)
        decrypted_message = f.decrypt(encrypted_message)
        if hashlib.md5(decrypted_message).hexdigest() != checksum:
            raise ValueError("Checksum does not match. Message may be corrupted.")
        return decrypted_message.decode()

# Usage
kms = KeyManagementService()
message = Message("header", "body", "footer", kms=kms)
encrypted_message, checksum = message.encode()
print(message.decode(encrypted_message, checksum))
