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
            decrypted_message = decrypt(values['encryption_method'], values['key'], data.decode('utf-8'))
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
        encrypted_message = encrypt(values['encryption_method'], values['key'], message)
        decrypted_message = decrypt(values['encryption_method'], values['key'], encrypted_message)
        update_chat(decrypted_message, chat, window)
        client_socket.sendall(bytes(encrypted_message, 'utf-8'))
    except: 
        sg.popup('Erro de conexão com a outra máquina!', title = 'Erro', icon='padlock_closed.ico')
    
def update_chat(message, chat, window):
    chat.append(message)   
    window['chat'].update(values = chat)

def update_status(window, status):    
    window['status_server'].update(status)

def create_layout(IP, chat):    
    layout = [
        [sg.Text('Meu IP: ' + IP), sg.Button('Hostear', key='start_server'), sg.Button('Encerrar', key='close_connection'), sg.Text('Status servidor:'), sg.Text('offline', key = 'status_server')],
        [sg.Text('IP:'), sg.Input(key='ip', do_not_clear=True, size=(25,25)), sg.Text('Criptografia:'), 
         sg.Combo(key='encryption_method', values=['S-DES', 'RC4'], enable_events=True), sg.Text('Chave:'), sg.Input(key='key', do_not_clear=True, size=(25,25)), sg.Button('Conectar', key='connect')],
        [sg.Listbox(key='chat', values = chat, size=(112, 25))],
        [sg.Input(key='message', do_not_clear=False, size=(106,25)), sg.Button('Enviar', key='send')]
    ]
    return layout

def update_key(value, window):
    if value == 'S-DES':
        window['key'].update('1000000000')
    if value == 'RC4':
        window['key'].update('teste')

def get_current_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    IP = s.getsockname()[0]
    s.close()
    return IP

def thread_server(IP, chat, window, q):
    server = threading.Thread(target=start_server, args=(IP, chat, window, q,))
    server.start()
                
def main():
    global close
    chat = []
    IP = get_current_ip()    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Layout
    layout = create_layout(IP, chat)
    window = sg.Window('Encrypted chat', layout, icon='padlock_closed.ico', finalize=True)
      
    thread_server(IP, chat, window)                 
       
    while True:
        global events, values
        events, values = window.read()   
        if events == sg.WINDOW_CLOSED:
            break
        if events == 'start_server' and window['status_server'].DisplayText == 'offline':          
            thread_server(IP, chat, window)  
        if events == 'close_connection':
            q.put(True)
        if events == 'encryption_method':
            update_key(values['encryption_method'], window)
        if events == 'connect':
            connect_client(client_socket, values['ip'])
        if events == 'send':
            send_message(client_socket, IP, values['message'], chat, window)

main()
