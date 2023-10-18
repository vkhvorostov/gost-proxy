from cipher.gost2015 import gost2015
import binascii

mtest = list(binascii.unhexlify('1122334455667700ffeeddccbbaa9988'))
ktest = list(binascii.unhexlify('8899aabbccddeeff0011223344556677fedcba98765432100123456789abcdef'))
print(binascii.unhexlify('8899aabbccddeeff0011223344556677fedcba98765432100123456789abcdef'))
gost = gost2015(ktest)
c = gost.encryption(mtest)
res = binascii.hexlify(bytearray(c))

print(res)

dtest = list(binascii.unhexlify(res))
d = gost.decryption(dtest)
dres = binascii.hexlify(bytearray(d))

print(dres)
