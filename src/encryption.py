import RC4
import SDES
import CBC

def encrypt(method, key, message):
    try:
        if method == 'RC4':
            return RC4.encrypt(key,  message)
        if method == 'S-DES':
            return SDES.encrypt(key,  message)
        if method == 'CBC':
            return CBC.encrypt(key,  message)
        return message
    except:
        return message

def decrypt(method, key, message):
    try:
        if method == 'RC4':
            return RC4.decrypt(key,  message)
        if method == 'S-DES':
            return SDES.decrypt(key,  message)
        if method == 'CBC':
            return CBC.decrypt(key,  message)
        return message
    except:
        return message