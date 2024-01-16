from cryptography.fernet import Fernet
import hashlib

class Message:
    def __init__(self, header, body, footer, metadata=None):
        self.header = header
        self.body = body
        self.footer = footer
        self.metadata = metadata if metadata else {}

    def encode(self, key):
        # Create a Fernet object
        cipher_suite = Fernet(key)

        # Encode the message
        encoded_message = self.body.encode('utf-8')

        # Encrypt the message
        encrypted_message = cipher_suite.encrypt(encoded_message)

        # Implement error detection mechanism
        # For example, we can use a checksum
        checksum = hashlib.md5(encoded_message).hexdigest()

        return encrypted_message, checksum

    def decode(self, encrypted_message, checksum, key):
        # Create a Fernet object
        cipher_suite = Fernet(key)

        # Decrypt the message
        decrypted_message = cipher_suite.decrypt(encrypted_message)

        # Implement error correction mechanism
        # For example, we can use the same checksum as in the encoding method
        if hashlib.md5(decrypted_message).hexdigest() != checksum:
            raise ValueError("Checksum does not match. The message may have been tampered with.")

        return decrypted_message.decode('utf-8')
