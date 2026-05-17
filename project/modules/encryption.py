"""
Encryption Module
Handles AES encryption and decryption operations
"""

from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Protocol.KDF import PBKDF2
import hashlib
from typing import Tuple


class EncryptionManager:
    """
    Manages encryption and decryption using AES
    """
    
    # AES encryption parameters
    KEY_SIZE = 32  # 256-bit key
    SALT_SIZE = 16  # 128-bit salt
    ITERATIONS = 100000  # PBKDF2 iterations
    
    @staticmethod
    def generate_key_from_password(password: str, salt: bytes = None) -> Tuple[bytes, bytes]:
        """
        Generate AES encryption key from password using PBKDF2
        
        Args:
            password (str): User password
            salt (bytes, optional): Salt for key derivation. If None, generates new salt.
            
        Returns:
            Tuple: (key, salt) - Encryption key and salt used
        """
        if salt is None:
            salt = get_random_bytes(EncryptionManager.SALT_SIZE)
        
        # Derive key using PBKDF2-SHA256
        def prf(p, s):
            return hashlib.sha256(p + s).digest()
        
        key = PBKDF2(password, salt, dkLen=EncryptionManager.KEY_SIZE, 
                     count=EncryptionManager.ITERATIONS, prf=prf)
        
        return key, salt
    
    @staticmethod
    def encrypt(data: bytes, password: str) -> bytes:
        """
        Encrypt data using AES-256 in GCM mode
        
        Args:
            data (bytes): Data to encrypt
            password (str): Encryption password
            
        Returns:
            bytes: Encrypted data (format: salt + nonce + ciphertext + tag)
        """
        # Generate key and salt
        key, salt = EncryptionManager.generate_key_from_password(password)
        
        # Create cipher in GCM mode
        cipher = AES.new(key, AES.MODE_GCM)
        nonce = cipher.nonce
        
        # Encrypt data
        ciphertext, tag = cipher.encrypt_and_digest(data)
        
        # Return salt + nonce + ciphertext + tag
        return salt + nonce + ciphertext + tag
    
    @staticmethod
    def decrypt(encrypted_data: bytes, password: str) -> bytes:
        """
        Decrypt AES-256 encrypted data
        
        Args:
            encrypted_data (bytes): Encrypted data (format: salt + nonce + ciphertext + tag)
            password (str): Decryption password
            
        Returns:
            bytes: Decrypted data
            
        Raises:
            ValueError: If decryption fails (wrong password or corrupted data)
        """
        try:
            # Extract salt and nonce
            salt = encrypted_data[:EncryptionManager.SALT_SIZE]
            nonce = encrypted_data[EncryptionManager.SALT_SIZE:EncryptionManager.SALT_SIZE + 16]
            ciphertext_and_tag = encrypted_data[EncryptionManager.SALT_SIZE + 16:]
            
            # Generate key from password and salt
            key, _ = EncryptionManager.generate_key_from_password(password, salt)
            
            # Create cipher with same nonce
            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
            
            # Decrypt and verify
            plaintext = cipher.decrypt_and_verify(ciphertext_and_tag[:-16], ciphertext_and_tag[-16:])
            
            return plaintext
            
        except (ValueError, KeyError) as e:
            raise ValueError("Decryption failed: Wrong password or corrupted data") from e
    
    @staticmethod
    def encrypt_text(text: str, password: str) -> bytes:
        """
        Encrypt text message
        
        Args:
            text (str): Text to encrypt
            password (str): Encryption password
            
        Returns:
            bytes: Encrypted text
        """
        return EncryptionManager.encrypt(text.encode('utf-8'), password)
    
    @staticmethod
    def decrypt_text(encrypted_data: bytes, password: str) -> str:
        """
        Decrypt encrypted text message
        
        Args:
            encrypted_data (bytes): Encrypted data
            password (str): Decryption password
            
        Returns:
            str: Decrypted text
        """
        plaintext = EncryptionManager.decrypt(encrypted_data, password)
        return plaintext.decode('utf-8')
    
    @staticmethod
    def encrypt_file(file_data: bytes, filename: str, password: str) -> bytes:
        """
        Encrypt file data with filename metadata
        
        Args:
            file_data (bytes): File content to encrypt
            filename (str): Original filename (including extension)
            password (str): Encryption password
            
        Returns:
            bytes: Encrypted data with metadata (format: marker + filename_len + filename + file_data)
        """
        # Encode filename
        filename_bytes = filename.encode('utf-8')
        
        # Create format: [0x01: marker][filename_length: 2 bytes][filename: variable][file_data: rest]
        metadata = b'\x01'  # File marker
        metadata += len(filename_bytes).to_bytes(2, byteorder='big')
        metadata += filename_bytes
        
        # Prepend metadata to file data
        full_data = metadata + file_data
        
        # Encrypt
        return EncryptionManager.encrypt(full_data, password)
    
    @staticmethod
    def decrypt_file(encrypted_data: bytes, password: str) -> Tuple[bytes, str]:
        """
        Decrypt encrypted file data with filename metadata
        
        Args:
            encrypted_data (bytes): Encrypted data
            password (str): Decryption password
            
        Returns:
            Tuple: (file_data, filename) - File content and original filename
            
        Raises:
            ValueError: If decryption fails
        """
        # Decrypt
        plaintext = EncryptionManager.decrypt(encrypted_data, password)
        
        # Check for file marker
        if len(plaintext) > 0 and plaintext[0] == 0x01:
            try:
                # Extract filename length
                filename_len = int.from_bytes(plaintext[1:3], byteorder='big')
                
                # Extract filename
                filename_start = 3
                filename_end = filename_start + filename_len
                filename = plaintext[filename_start:filename_end].decode('utf-8')
                
                # Extract file data
                file_data = plaintext[filename_end:]
                
                return file_data, filename
                
            except (ValueError, UnicodeDecodeError) as e:
                raise ValueError(f"Failed to extract file metadata: {str(e)}") from e
        else:
            # No file marker - treat as text or generic data
            raise ValueError("No file metadata found in encrypted data")
