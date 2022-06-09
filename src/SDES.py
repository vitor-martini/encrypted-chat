import math

S0 = [[ 1, 0, 3, 2],
      [3, 2, 1, 0],
      [0, 2, 1, 3],
      [3, 1, 3, 2]]

S1 = [[ 1, 1, 2, 3],
      [2, 0, 1, 3],
      [3, 0, 1, 0],
      [2, 1, 0, 3]]

key_1 = ''
key_2 = ''

def generate_keys(key):
    global key_1, key_2
    key = shift(P10(key))
    key_1 = P8(key)
    key_2 = P8(shift(shift(key)))

def encrypt(key, plain_text):
    binary = string_to_binary(plain_text)
    list_of_bytes = binary_to_list(binary)
    encrypted_text = ""

    generate_keys(key)
    for bytes in list_of_bytes:
        encrypted_text += reverse_IP(F(swap(F(IP(bytes), key_1)), key_2))

    return binary_to_string(encrypted_text)

def decrypt(key, encrypted_text):
    encrypted_text = string_to_binary(encrypted_text)
    list_of_bytes = binary_to_list(encrypted_text)
    decrypted_text = ""

    generate_keys(key)
    for bytes in list_of_bytes:
        decrypted_text += reverse_IP(F(swap(F(IP(bytes), key_2)), key_1))

    return binary_to_string(decrypted_text)

def P10(key):    
    permutated_key = (
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

    return permutated_key

def shift(key):
    key_left = shift_table(key[0:5])
    key_right = shift_table(key[5:10])
    return key_left + key_right

def shift_table(key):
    return (key[1] + 
            key[2] + 
            key[3] + 
            key[4] + 
            key[0])

def P8(key):
    permutated_key = (
        key[5] + 
        key[2] + 
        key[6] + 
        key[3] + 
        key[7] + 
        key[4] + 
        key[9] + 
        key[8])
    return permutated_key

def IP(message):
    permutated_message = (
        message[1] + 
        message[5] + 
        message[2] + 
        message[0] + 
        message[3] + 
        message[7] + 
        message[4] + 
        message[6])

    return permutated_message

def F(message, K):
    left = message[0:4]
    right = message[4:8]
    new_values = XOR(P4(blocks(XOR(expansion(right), K))), left)

    return new_values + right

def expansion(message):    
    message_expanded = (
        message[3] + 
        message[0] + 
        message[1] + 
        message[2] + 
        message[1] + 
        message[2] + 
        message[3] + 
        message[0])
    return message_expanded

def XOR(left, right):    
    result = ""
    for i in range(len(left)):
        if (left[i]== '1' and right[i]== '0') or (left[i]== '0' and right[i]== '1'): result += '1'        
        else: result += '0'    

    return result

def int_to_binary(i):       
    binary = ""    
    if(i == 0): binary = "00"    
    if(i == 1): binary = "01"    
    if(i == 2): binary = "10"
    if(i == 3): binary = "11"

    return binary

def blocks(message):
    
    message_left = message[0:4]    
    S0_row = int(message_left[0] + message_left[3], 2)
    S0_column = int(message_left[1] + message_left[2], 2)

    message_right = message[4:8]     
    S1_row = int(message_right[0] + message_right[3], 2)
    S1_column = int(message_right[1] + message_right[2], 2)

    S0_cell = int_to_binary(S0[S0_row][S0_column])    
    S1_cell = int_to_binary(S1[S1_row][S1_column])
    return S0_cell + S1_cell

def P4(message):       
    permutated_message = (
        message[1] + 
        message[3] + 
        message[2] + 
        message[0])
    return permutated_message

def swap(message):
    swapped_message = message[4:8] + message[0:4]
    return swapped_message

def reverse_IP(message):
    permutated_message = (
        message[3] + 
        message[0] + 
        message[2] + 
        message[4] + 
        message[6] + 
        message[1] + 
        message[7] + 
        message[5])
    return permutated_message

def string_to_binary(text):  
    ascii_table, result = [], []

    for character in text:
        ascii_table.append(ord(character))

    for i in ascii_table:
        result.append(str(bin(i)[2:])[::-1].ljust(8, "0")[::-1])

    return ''.join(result)

def binary_to_list(binary):
    list_of_bytes = []
    i = 0
    while i < len(binary):
        list_of_bytes.append(binary[i:i+8])
        i += 8

    return list_of_bytes

def binary_to_string(text):
    ascii_table = []
    list_of_bytes = binary_to_list(text)
    result = ""

    for i in list_of_bytes:
        aux, ascii_character = 0, 0
        i = int(i)
        k = int(math.log10(i)) + 1

        for j in range(k):
            aux = ((i % 10) * (2**j))   
            i = i // 10
            ascii_character = ascii_character + aux

        ascii_table.append(ascii_character)

    for ascii_character in ascii_table:
        result += chr(ascii_character)
    return result
