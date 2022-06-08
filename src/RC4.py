import codecs

MOD = 256

def swap(S, i, j):
    S[i], S[j] = S[j], S[i]

def KSA(key):
    key_length = len(key)
    S = list(range(MOD))  
    j = 0
    for i in range(MOD):
        j = (j + S[i] + key[i % key_length]) % MOD
        swap(S, i, j)  

    return S

def PRGA(S):
    i = 0
    j = 0
    while True:
        i = (i + 1) % MOD
        j = (j + S[i]) % MOD

        swap(S, i, j)  
        K = S[(S[i] + S[j]) % MOD]
        yield K

def encrypt(key, text, decrypt=False):
    if decrypt == False: text = [ord(byte) for byte in text]
    key = [ord(byte) for byte in key]    
    keystream = PRGA(KSA(key))

    cipher_text = []
    for byte in text:
        val = ("%02X" % (byte ^ next(keystream)))  
        cipher_text.append(val)
    return ''.join(cipher_text)

def decrypt(key, cipher_text):
    cipher_text = codecs.decode(cipher_text, 'hex_codec')
    decrypted_text = encrypt(key, cipher_text, True)
    return codecs.decode(decrypted_text, 'hex_codec').decode('utf-8')

# def main():
#     plaintext = input('plaintext: ')
#     key = input('key: ')
#     ecrypted = encrypt(key, plaintext)
#     decrypted = decrypt(key, ecrypted)

#     print('cifrado: ' + ecrypted)
#     print('descifrado: ' + decrypted)
    
# main()