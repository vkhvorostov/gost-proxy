from cipher.gost2015 import gost2015

def kuznyechik_encrypt(gost, plaintext: bytes):
    ciphertext = bytearray()
    
    for i in range(0, len(plaintext), 16):
        block = plaintext[i:i+16].ljust(16, b'\0')  # Pad the last block if needed
        bytes_block = list(block)
        encrypted_block = gost.encryption(bytes_block)
        ciphertext.extend(encrypted_block)
    
    return bytes(ciphertext)

def kuznyechik_decrypt(gost, ciphertext: bytes):
    plaintext = bytearray()
    
    for i in range(0, len(ciphertext), 16):
        block = ciphertext[i:i+16]
        bytes_block = bytes_block = list(block)
        decrypted_block = gost.decryption(bytes_block)
        plaintext.extend(decrypted_block)
    
    return bytes(plaintext)


mtest = '{"data": "Hello world"}'.encode('utf-8')
ktest = list(bytes.fromhex('8899aabbccddeeff0011223344556677fedcba98765432100123456789abcdef'))
gost = gost2015(ktest)
c = kuznyechik_encrypt(gost, mtest)
res = bytearray(c).hex()

print(mtest)
print(res)

dtest = bytes.fromhex(res)
d = kuznyechik_decrypt(gost, dtest)
dres = bytearray(d).decode('utf-8')

print(dres)
