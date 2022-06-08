from curses import keyname
from PySimpleGUI import PySimpleGUI as sg
import RC4
import socket
import threading

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

def start_server(IP, chat, window):  
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((IP, 3000))
        server_socket.listen()
        update_status(window, 'online')
           
        server, addr = server_socket.accept()
        while True:            
            data = server.recv(1024)
            decrypted_message = decrypt(method, key, data.decode('utf-8'))
            update_chat(decrypted_message, chat, window) 
                        
            if not data:
                break
            server.sendall(data)
        server.shutdown()
        server.close()
    except:
        update_status(window, 'offline')

def connect_client(client_socket, IP):
    try:
        client_socket.connect((IP, 3000))
        sg.popup('Conexão com a outra máquina feita com sucesso!', title = 'Sucesso', icon='padlock_closed.ico')    
    except: 
        sg.popup('Erro de conexão com a outra máquina!', title = 'Erro', icon='padlock_closed.ico')
    
def send_message(client_socket, IP, message, chat, window):
    try:
        message = IP + ': ' + message
        encrypted_message = encrypt(method, key, message)
        decrypted_message = decrypt(method, key, encrypted_message)
        update_chat(decrypted_message, chat, window)
        client_socket.sendall(bytes(encrypted_message, 'utf-8'))
    except: 
        sg.popup('Erro de conexão com a outra máquina!', title = 'Erro', icon='padlock_closed.ico')
    
def update_chat(message, chat, window):
    chat.append(message)   
    window['chat'].update(values = chat)

def update_status(window, status):    
    window['status_server'].update(status)
    if status == 'online': window['status_server'].Update(text_color='green')
    if status == 'offline': window['status_server'].Update(text_color='red')

def create_layout(IP, chat):    
    layout = [
        [sg.Text('Meu IP: ' + IP), sg.Text('Status servidor:'), sg.Text('offline', key = 'status_server', text_color='red'), sg.Button('Hostear', key='start_server', size=(10,1)), sg.Button('Encerrar', key='close_connection', size=(10,1))],
        [sg.Text('IP:'), sg.Input(key='ip', do_not_clear=True, size=(53,25)), sg.Button('Conectar', key='connect', size=(10,1))],
        [sg.Text('Criptografia:'), sg.Combo(key='encryption_method', values=['S-DES', 'RC4'], enable_events=True, size=(10,1)), sg.Text('Chave:'), sg.Input(key='key', do_not_clear=True, size=(23,25)), sg.Button('Aplicar', key='apply', size=(10,1))],
        [sg.Listbox(key='chat', values = chat, size=(70, 25))],
        [sg.Input(key='message', do_not_clear=False, size=(56,25)), sg.Button('Enviar', key='send', size=(10,1))]
    ]
    return layout

def update_key(value, window):
    if value == 'S-DES':
        window['key'].update('1000000000')
    if value == 'RC4':
        window['key'].update('teste')

def update_cryptography(_method, _key):
    global method, key
    method = _method
    key = _key

def get_current_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    IP = s.getsockname()[0]
    s.close()
    return IP

def thread_server(IP, chat, window):
    server = threading.Thread(target=start_server, args=(IP, chat, window,))
    server.start()
                
def main():
    global method, key
    method = ''
    key = ''
    chat = []
    IP = get_current_ip()    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Layout
    layout = create_layout(IP, chat)
    window = sg.Window('Encrypted chat', layout, icon='padlock_closed.ico', finalize=True)
                     
    while True:
        events, values = window.read()   
        if events == sg.WINDOW_CLOSED:
            break
        if events == 'start_server' and window['status_server'].DisplayText == 'offline':          
            thread_server(IP, chat, window)  
        if events == 'connect':
            connect_client(client_socket, values['ip'])
        if events == 'apply':
            update_cryptography(values['encryption_method'], values['key'])
        if events == 'send':
            send_message(client_socket, IP, values['message'], chat, window)

main()
