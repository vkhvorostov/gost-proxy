from cipher.gost2015 import gost2015

class text_cipher:
    def __init__(self, key: str, algorithm: str):
        if algorithm == 'kuznechik':
            self.algorithm = algorithm
            self.key = list(bytes.fromhex(key))
            self.cipher = gost2015(self.key)
        else:
            raise ValueError('Not supported algorithm ' + algorithm)    

    def encrypt(self, plaintext: bytes):
        if self.algorithm == 'kuznechik':
            ciphertext = bytearray()
    
            for i in range(0, len(plaintext), 16):
                block = plaintext[i:i+16].ljust(16, b'\0') # Pad the last block if needed
                bytes_block = list(block)
                encrypted_block = self.cipher.encryption(bytes_block)
                ciphertext.extend(encrypted_block)
            
            return bytes(ciphertext)
        
    def decrypt(self, ciphertext: bytes):
        if self.algorithm == 'kuznechik':
            plaintext = bytearray()
            
            for i in range(0, len(ciphertext), 16):
                block = ciphertext[i:i+16]
                bytes_block = list(block)
                decrypted_block = self.cipher.decryption(bytes_block)
                plaintext.extend(decrypted_block)
            
            plaintext = plaintext.rstrip(b'\0')
            return bytes(plaintext)
