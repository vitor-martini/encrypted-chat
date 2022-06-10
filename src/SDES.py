from binary_operations import string_to_binary, binary_to_list, binary_to_string, XOR, int_to_binary

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

def SDES(message, key_1, key_2):
    return reverse_IP(F(swap(F(IP(message), key_1)), key_2))

def encrypt(key, message):
    generate_keys(key)
    list_of_bytes = binary_to_list(string_to_binary(message))
    encrypted_message = []

    for bytes in list_of_bytes:
        encrypted_message.append(SDES(bytes, key_1, key_2))

    return "".join(encrypted_message)

def decrypt(key, encrypted_message):
    generate_keys(key)
    encrypted_message = binary_to_list(encrypted_message)
    decrypted_message = []

    for bytes in encrypted_message:
        decrypted_message.append(SDES(bytes, key_2, key_1))

    return binary_to_string("".join(decrypted_message))
