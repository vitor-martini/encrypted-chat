import math

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
