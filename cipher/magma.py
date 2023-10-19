# Magma (GOST) Block Cipher

# Russian
# https://web.archive.org/web/20150924113434/http://tc26.ru/standard/gost/GOST_R_3412-2015.pdf

# English
# https://en.wikipedia.org/wiki/GOST_(block_cipher)

class magma:
	
    def __init__(self, key):

        pi0 = [12, 4, 6, 2, 10, 5, 11, 9, 14, 8, 13, 7, 0, 3, 15, 1]
        pi1 = [6, 8, 2, 3, 9, 10, 5, 12, 1, 14, 4, 7, 11, 13, 0, 15]
        pi2 = [11, 3, 5, 8, 2, 15, 10, 13, 14, 1, 7, 4, 12, 9, 6, 0]
        pi3 = [12, 8, 2, 1, 13, 4, 15, 6, 7, 0, 10, 5, 3, 14, 9, 11]
        pi4 = [7, 15, 5, 10, 8, 1, 6, 13, 0, 9, 3, 14, 11, 4, 2, 12]
        pi5 = [5, 13, 15, 6, 9, 2, 12, 10, 11, 7, 8, 1, 4, 3, 14, 0]
        pi6 = [8, 14, 2, 5, 6, 9, 1, 12, 15, 4, 11, 0, 13, 10, 3, 7]
        pi7 = [1, 7, 14, 13, 0, 5, 8, 3, 4, 15, 10, 6, 9, 12, 11, 2]

        self.pi = [pi0, pi1, pi2, pi3, pi4, pi5, pi6, pi7]
        self.key = key
        self.MASK32 = 2 ** 32 - 1

    # The input value x is 32 bits
    # The return value y is 32-bits
    def t(self, x):
        y = 0
        for i in reversed(range(8)):
            j = (x >> 4 * i) & 0xf
            y <<= 4
            y ^= self.pi[i][j]
        return y


    # x is 32-bit integer 
    def rot11(self, x):
        return ((x << 11) ^ (x >> (32 - 11))) & self.MASK32


    # x and k are 32-bit integers
    def g(self, x, k):
        return self.rot11(self.t((x + k) % 2 ** 32))


    # x is 64 bits
    # The return value is given as a tuple and is 
    # the left 32-bits and the right 32-bits of x
    def split(self, x):
        L = x >> 32
        R = x & self.MASK32
        return (L, R)


    # L and R are 32-bits
    # The return value is 64-bits 
    # obtained by concatenating L and R
    def join(self, L, R):
        return (L << 32) ^ R


    # k is 256-bits. 
    # The return value is a list of 32 keys of 32-bits each.
    # The first 8 keys just come from the key k 
    # by partitioning k into eight 32-bit segments.
    # The remaining keys are just repeats of these first 8 keys.
    def key_schedule(self):
            k = self.key
            keys = []
            for i in reversed(range(8)):
                keys.append((k >> (32 * i)) & self.MASK32)
            for i in range(8):
                keys.append(keys[i])
            for i in range(8):
                keys.append(keys[i])
            for i in reversed(range(8)):
                keys.append(keys[i])
            return keys



    # The input value x (the plaintext) is 64 bits.
    # k is 256 bits
    # The return value (the ciphertext) is 64-bits
    def encrypt(self, x):
        keys = self.key_schedule()
        (L, R) = self.split(x)
        for i in range(31):
                (L, R) = (R, L ^ self.g(R, keys[i]))
        return self.join(L ^ self.g(R, keys[-1]), R)


    # The input value x (the ciphertext) is 64 bits.
    # k is 256 bits
    # The return value (the plaintext) is 64-bits
    def decrypt(self, x):
        keys = self.key_schedule()
        keys.reverse()
        (L, R) = self.split(x)
        for i in range(31):
                (L, R) = (R, L ^ self.g(R, keys[i]))
        return self.join(L ^ self.g(R, keys[-1]), R)