from cryptography.fernet import Fernet
import hashlib

class KeyManagementService:
    def generate_key(self):
        # This is a placeholder implementation. In a real-world scenario, you'd want a more secure method.
        return Fernet.generate_key()

    def get_key(self):
        # This is a placeholder implementation. In a real-world scenario, you'd want a more secure method.
        return Fernet.generate_key()

class Message:
    def __init__(self, header, body, footer, metadata=None, kms=None):
        self.header = header
        self.body = body
        self.footer = footer
        self.metadata = metadata if metadata else {}
        self.kms = kms  # Key Management Service

    def encode(self):
        key = self.kms.generate_key()  # Generate a new key
        f = Fernet(key)
        encrypted_message = f.encrypt(self.body.encode())
        checksum = hashlib.md5(encrypted_message).hexdigest()
        return encrypted_message, checksum

    def decode(self, encrypted_message, checksum):
        key = self.kms.get_key()  # Get the key
        f = Fernet(key)
        decrypted_message = f.decrypt(encrypted_message)
        if hashlib.md5(encrypted_message).hexdigest() != checksum:
            raise ValueError("Checksum does not match. Message may be corrupted.")
        return decrypted_message.decode()

# Usage
kms = KeyManagementService()
message = Message("header", "body", "footer", kms=kms)
encrypted_message, checksum = message.encode()
print(message.decode(encrypted_message, checksum))
