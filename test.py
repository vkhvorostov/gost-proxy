from cipher.text_cipher import text_cipher


algorithm = 'kuznechik'
key = '8899aabbccddeeff0011223344556677fedcba98765432100123456789abcdef'
cipher = text_cipher(key, algorithm)

print('kuznechik test with gost example string')
text = '1122334455667700ffeeddccbbaa9988'
print(text)
res = cipher.encrypt(bytes.fromhex(text)) # Convert input to bytes string
print(res.hex()) # Convert result from bytes to hex string
print()

print('kuznechik test with real string')
text = '{"data": "Привет мир"}'
print(text)
res = cipher.encrypt(text.encode('utf-8')) # Convert tex input to bytes string
print(res.hex())
dres = cipher.decrypt(res)
print(dres.decode('utf-8')) # Convert result to plain string
print()


algorithm = 'magma'
key = 'ffeeddccbbaa99887766554433221100f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff'
cipher = text_cipher(key, algorithm)

print('magma test with gost example string')
text = 'fedcba9876543210'
print(text)
res = cipher.encrypt(bytes.fromhex(text))
print(res.hex())
print()

print('magma test with real string')
text = '{"data": "Привет мир"}'
print(text)
res = cipher.encrypt(text.encode('utf-8'))
print(res.hex())
dres = cipher.decrypt(res)
print(dres.decode('utf-8'))
