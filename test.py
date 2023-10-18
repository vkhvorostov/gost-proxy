from cipher.text_cipher import text_cipher

algorithm = 'kuznechik'
key = '8899aabbccddeeff0011223344556677fedcba98765432100123456789abcdef'
text = '{"data": "Hello world"}'.encode('utf-8') # Convert to bytes string
print(text)
cipher = text_cipher(key, algorithm)
res = cipher.encrypt(text)
print(res.hex()) # Convert result to hex string
dres = cipher.decrypt(res)
print(dres.decode('utf-8')) # Convert result to plain string