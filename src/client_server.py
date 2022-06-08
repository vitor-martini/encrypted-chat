import socket
import threading
import layout 
from PySimpleGUI import PySimpleGUI as sg
from layout import update_status, update_chat
from encryption import encrypt, decrypt

def thread_server(IP, chat, window):
    server = threading.Thread(target=start_server, args=(IP, chat, window,))
    server.start()

def start_server(IP, chat, window):      
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((IP, 3000))
        server_socket.listen()
        update_status(window, 'online')
           
        while True:    
            server, addr = server_socket.accept()
            data = server.recv(1024)
            if data.decode('utf-8') == 'exit':
                break
            decrypted_message = decrypt(layout.method, layout.key, data.decode('utf-8'))
            update_chat(decrypted_message, chat, window)             
            
            server.sendall(data)
        server.close()
    except:
        update_status(window, 'offline')

def stop_server(IP):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((IP, 3000))
    server_socket.sendall(bytes('exit', 'utf-8'))

def connect_client(IP, IP_cliente):
    if IP == IP_cliente:
        sg.popup('Informe outro IP!', title = 'Erro', icon='padlock_closed.ico')
        return 
        
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP_cliente, 3000))
    return client_socket
    
def send_message(IP, IP_cliente, message, chat, window):
    try:        
        client_socket = connect_client(IP, IP_cliente)

        message = IP + ': ' + message        
        encrypted_message = encrypt(layout.method, layout.key, message)
        decrypted_message = decrypt(layout.method, layout.key, encrypted_message)

        client_socket.sendall(bytes(encrypted_message, 'utf-8'))
        update_chat(decrypted_message, chat, window)
    except: 
        sg.popup('Erro de conexão!', title = 'Erro', icon='padlock_closed.ico')
    
def get_current_ip():
    current_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    current_server.connect(("8.8.8.8", 80))
    IP = current_server.getsockname()[0]
    current_server.close()
    return IP