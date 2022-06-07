S0 = [[ 1, 0, 3, 2],
        [3, 2, 1, 0],
        [0, 2, 1, 3],
        [3, 1, 3, 2]]

S1 = [[ 1, 1, 2, 3],
        [2, 0, 1, 3],
        [3, 0, 1, 0],
        [2, 1, 0, 3]]

key1 = ''
key2 = ''

def generate_keys(key):
    global key1, key2
    key = shift(P10(key))
    key1 = P8(key)
    key2 = P8(shift(shift(key)))

def encrypt(key, plain_text):
    generate_keys(key)
    return IPReverse(F(swap(F(IP(plain_text), key1)), key2))

def decrypt(key, plain_text):
    generate_keys(key)
    return IPReverse(F(swap(F(IP(plain_text), key2)), key1))

def P10(key):    
    permutatedKey = (
        key[2] + 
        key[4] + 
        key[1] + 
        key[6] + 
        key[3] + 
        key[9] + 
        key[0] + 
        key[8] + 
        key[7] + 
        key[5])

    return permutatedKey

def shift(key):
    keyLeft = shiftTable(key[0:5])
    keyRight = shiftTable(key[5:10])
    return keyLeft + keyRight

def shiftTable(key):
    return (key[1] + 
            key[2] + 
            key[3] + 
            key[4] + 
            key[0])

def P8(key):
    permutatedKey = (
        key[5] + 
        key[2] + 
        key[6] + 
        key[3] + 
        key[7] + 
        key[4] + 
        key[9] + 
        key[8])
    return permutatedKey

def IP(message):
    permutatedMessage = (
        message[1] + 
        message[5] + 
        message[2] + 
        message[0] + 
        message[3] + 
        message[7] + 
        message[4] + 
        message[6])

    return permutatedMessage

def F(message, K):
    left = message[0:4]
    right = message[4:8]
    newValues = XOR(P4(blocks(XOR(expansion(right), K))), left)

    return newValues + right

def expansion(message):
    
    messageExpanded = (
        message[3] + 
        message[0] + 
        message[1] + 
        message[2] + 
        message[1] + 
        message[2] + 
        message[3] + 
        message[0])
    return messageExpanded

def XOR(left, right):    
    binaryXOR = ""
    for i in range(len(left)):
        if (left[i]== '1' and right[i]== '0') or (left[i]== '0' and right[i]== '1'): binaryXOR += '1'        
        else: binaryXOR += '0'    

    return binaryXOR

def intToBinary(i):       
    binary = ""    
    if(i == 0): binary = "00"    
    if(i == 1): binary = "01"    
    if(i == 2): binary = "10"
    if(i == 3): binary = "11"

    return binary

def blocks(message):
    
    messageLeft = message[0:4]    
    S0Row = int(messageLeft[0] + messageLeft[3], 2)
    S0Column = int(messageLeft[1] + messageLeft[2], 2)

    messageRight = message[4:8]     
    S1Row = int(messageRight[0] + messageRight[3], 2)
    S1Column = int(messageRight[1] + messageRight[2], 2)

    S0Cell = intToBinary(S0[S0Row][S0Column])    
    S1Cell = intToBinary(S1[S1Row][S1Column])
    return S0Cell + S1Cell

def P4(message):       
    permutatedMessage = (
        message[1] + 
        message[3] + 
        message[2] + 
        message[0])
    return permutatedMessage

def swap(message):
    swappedMessage = message[4:8] + message[0:4]
    return swappedMessage

def IPReverse(message):
    permutatedMessage = (
        message[3] + 
        message[0] + 
        message[2] + 
        message[4] + 
        message[6] + 
        message[1] + 
        message[7] + 
        message[5])
    return permutatedMessage

def main():
    plaintext = input('plaintext: ')
    key = input('key: ')
    ecrypted = encrypt(key, plaintext)
    decrypted = decrypt(key, ecrypted)

    print('cifrado: ' + ecrypted)
    print('descifrado: ' + decrypted)




main()