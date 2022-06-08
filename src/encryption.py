import RC4

def encrypt(method, key, message):
    if method == 'RC4':
        return RC4.encrypt(key,  message)
    return message

def decrypt(method, key, message):
    try:
        if method == 'RC4':
            return RC4.decrypt(key,  message)
        return message
    except:
        return message