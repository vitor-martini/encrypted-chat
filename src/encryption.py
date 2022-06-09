import RC4
import SDES

def encrypt(method, key, message):
    if method == 'RC4':
        return RC4.encrypt(key,  message)
    if method == 'S-DES':
        return SDES.encrypt(key,  message)
    return message

def decrypt(method, key, message):
    try:
        if method == 'RC4':
            return RC4.decrypt(key,  message)
        if method == 'S-DES':
            return SDES.decrypt(key,  message)
        return message
    except:
        return message