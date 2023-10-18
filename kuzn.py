import struct

def kuznyechik_encrypt_block(key, block):
    def lsh(n, x):
        return ((x << n) & 0xFFFFFFFFFFFFFFFF) | (x >> (64 - n))

    def rsh(n, x):
        return (x >> n) | ((x & (2**n - 1)) << (64 - n))

    def add_mod_2_64(x, y):
        result = x + y
        if result > 0xFFFFFFFFFFFFFFFF:
            result -= 0xFFFFFFFFFFFFFFFF
        return result

    key_schedule = [struct.unpack("<Q", key[i:i+8])[0] for i in range(0, len(key), 8)]

    for round_num in range(10):
        for i in range(0, len(key_schedule)):
            left, right = struct.unpack("<QQ", block)

            round_key = key_schedule[i]
            t = add_mod_2_64(left, round_key)
            t = lsh(1, t)
            right ^= t

            t = add_mod_2_64(left, round_key)
            t = lsh(1, t)
            right ^= t

            right = rsh(8, right)
            left = lsh(8, left)
            left ^= right

            block = struct.pack("<QQ", left, right)

        block = block[8:] + block[:8]

    return block

def kuznyechik_decrypt_block(key, block):
    def lsh(n, x):
        return ((x << n) & 0xFFFFFFFFFFFFFFFF) | (x >> (64 - n))

    def rsh(n, x):
        return (x >> n) | ((x & (2**n - 1)) << (64 - n))

    def add_mod_2_64(x, y):
        result = x + y
        if result > 0xFFFFFFFFFFFFFFFF:
            result -= 0xFFFFFFFFFFFFFFFF
        return result

    key_schedule = [struct.unpack("<Q", key[i:i+8])[0] for i in range(0, len(key), 8)]

    for round_num in range(10):
        for i in range(len(key_schedule) - 1, -1, -1):
            left, right = struct.unpack("<QQ", block)

            round_key = key_schedule[i]
            left ^= right
            right = rsh(8, right)
            left = lsh(8, left)

            t = add_mod_2_64(left, round_key)
            t = rsh(1, t)
            right ^= t

            t = add_mod_2_64(left, round_key)
            t = rsh(1, t)
            right ^= t

            block = struct.pack("<QQ", left, right)

        block = block[8:] + block[:8]

    return block

def kuznyechik_encrypt(key, plaintext):
    if len(key) != 32:
        raise ValueError("The key should be 32 bytes (256 bits) long.")
    
    ciphertext = bytearray()
    
    for i in range(0, len(plaintext), 16):
        block = plaintext[i:i+16].ljust(16, b'\0')  # Pad the last block if needed
        encrypted_block = kuznyechik_encrypt_block(key, block)
        ciphertext.extend(encrypted_block)
    
    return bytes(ciphertext)

def kuznyechik_decrypt(key, ciphertext):
    if len(key) != 32:
        raise ValueError("The key should be 32 bytes (256 bits) long.")
    
    plaintext = bytearray()
    
    for i in range(0, len(ciphertext), 16):
        block = ciphertext[i:i+16]
        decrypted_block = kuznyechik_decrypt_block(key, block)
        plaintext.extend(decrypted_block)
    
    return bytes(plaintext)

# Example usage:
key = bytes.fromhex("8899aabbccddeeff0011223344556677fedcba98765432100123456789abcdef")
plaintext = bytes.fromhex("1122334455667700ffeeddccbbaa9988")
ciphertext = kuznyechik_encrypt(key, plaintext)
print("Ciphertext:", ciphertext.hex())

decrypted_text = kuznyechik_decrypt(key, ciphertext)
print("Decrypted Text:", decrypted_text.hex())
