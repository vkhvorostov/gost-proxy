from cipher.gost2015 import gost2015
from cipher.magma import magma

class text_cipher:
    def __init__(self, key: str, algorithm: str):
        self.algorithm = algorithm
        if algorithm == 'kuznechik':
            key = list(bytes.fromhex(key))
            self.cipher = gost2015(key)
        elif algorithm == 'magma':
            key = int(key, 16)
            self.cipher = magma(key)
        else:
            raise ValueError('Not supported algorithm ' + algorithm)    

    def encrypt(self, plaintext: bytes):
        ciphertext = bytearray()
        if self.algorithm == 'kuznechik':
            for i in range(0, len(plaintext), 16):
                block = plaintext[i:i+16].ljust(16, b'\0') # Pad the last block if needed
                bytes_block = list(block)
                encrypted_block = self.cipher.encryption(bytes_block)
                ciphertext.extend(encrypted_block)
        elif self.algorithm == 'magma':
            for i in range(0, len(plaintext), 8):
                block = plaintext[i:i+8].ljust(8, b'\0') # Pad the last block if needed
                int_block = int.from_bytes(block)
                encrypted_block = self.cipher.encrypt(int_block)
                hex_block = f"{encrypted_block:x}"
                ciphertext.extend(bytes.fromhex(hex_block))       
        return bytes(ciphertext)
        
    def decrypt(self, ciphertext: bytes):
        plaintext = bytearray()
        if self.algorithm == 'kuznechik':            
            for i in range(0, len(ciphertext), 16):
                block = ciphertext[i:i+16]
                bytes_block = list(block)
                decrypted_block = self.cipher.decryption(bytes_block)
                plaintext.extend(decrypted_block)
        elif self.algorithm == 'magma':    
            for i in range(0, len(ciphertext), 8):
                block = ciphertext[i:i+8]
                int_block = int.from_bytes(block)
                decrypted_block = self.cipher.decrypt(int_block)
                hex_block = f"{decrypted_block:x}"
                plaintext.extend(bytes.fromhex(hex_block))       
        plaintext = plaintext.rstrip(b'\0')
        return bytes(plaintext)
