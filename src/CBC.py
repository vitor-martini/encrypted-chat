from SDES import generate_keys, SDES_function, XOR, validade_key, correct_key
import SDES
from binary_operations import binary_to_list,  binary_to_string, string_to_binary

def encrypt(key, message):
    key = str(key)
    if validade_key(key) == False:
        key = correct_key(key)
    generate_keys(key)
    IV = '10101010'
    binary_message = binary_to_list(string_to_binary(message))
    encrypted_message = [SDES_function(XOR(binary_message[0], IV), SDES.key_1, SDES.key_2)]

    for i in range(1, len(binary_message)):
        encrypted_message.append(SDES_function(XOR(binary_message[i], encrypted_message[i-1]), SDES.key_1, SDES.key_2))

    return "".join(encrypted_message)

def decrypt(key, encrypted_message):
    key = str(key)
    if validade_key(key) == False:
        key = correct_key(key)
    generate_keys(key)
    IV = '10101010'
    encrypted_message = binary_to_list(encrypted_message)
    decrypted_message = [XOR(SDES_function(encrypted_message[0], SDES.key_2, SDES.key_1), IV)]

    for i in range(1, len(encrypted_message)):
        decrypted_message.append(XOR(SDES_function(encrypted_message[i], SDES.key_2, SDES.key_1), encrypted_message[i-1]))

    return binary_to_string("".join(decrypted_message))