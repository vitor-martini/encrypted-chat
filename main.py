from PySimpleGUI import PySimpleGUI as sg
import socket
import threading

def start_server(IP, chat, window):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((IP, 3000))
        server_socket.listen()

        server, addr = server_socket.accept()
        while 1:
            data = server.recv(1024)
            update_chat(data.decode('utf-8'), chat, window)
            if not data:
                break
            server.sendall(data)
        server.close()
    except:
        server.close()

def connect_client(client_socket, IP):
    try:
        client_socket.connect((IP, 3000))
        sg.popup('Conexão feita com sucesso!', title = 'Sucesso', icon='padlock_closed.ico')    
    except: 
        sg.popup('Erro de conexão!', title = 'Erro', icon='padlock_closed.ico')
    
def send_message(client_socket, IP, message, chat, window):
    try:
        message = IP + ': ' + message
        update_chat(message, chat, window)
        client_socket.sendall(bytes(message, 'utf-8'))
    except: 
        sg.popup('Erro de conexão!', title = 'Erro', icon='padlock_closed.ico')
    
def update_chat(message, chat, window):
    chat.append(message)   
    window['chat'].update(values = chat)

def create_layout(IP, chat):    
    layout = [
        [sg.Text('Meu IP: ' + IP)],
        [sg.Text('IP:'), sg.Input(key='ip', do_not_clear=True, size=(25,25)), sg.Text('Criptografia:'), 
         sg.Combo(key='combo', values=['S-DES', 'RC4'], enable_events=True), sg.Text('Chave:'), sg.Input(key='key', do_not_clear=True, size=(25,25)), sg.Button('Conectar', key='connect')],
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
    
def main():
    chat = []
    IP = get_current_ip()    

    # Layout
    layout = create_layout(IP, chat)
    window = sg.Window('Encrypted chat', icon='padlock_closed.ico').Layout(layout)    
    
    # Conexão
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server = threading.Thread(target=start_server, args=(IP, chat, window,))
    server.start()

    while True:
        events, values = window.read()
        if events == sg.WINDOW_CLOSED:
            break
        if events == 'combo':
            update_key(values['combo'], window)
        if events == 'connect':
            connect_client(client_socket, values['ip'])
        if events == 'send':
            send_message(client_socket, IP, values['message'], chat, window)

main()
