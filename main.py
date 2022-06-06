from nis import cat
from PySimpleGUI import PySimpleGUI as sg
import socket
import threading

def start_server():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((IP, 3000))
        server_socket.listen()

        server, addr = server_socket.accept()
        while 1:
            data = server.recv(1024)
            update_chat(data.decode('utf-8'))
            if not data:
                break
            server.sendall(data)
        server.close()
    except:
        server.close()

def connect_client(IP):
    try:
        client_socket.connect((IP, 3000))
        sg.popup('Conexão feita com sucesso!', title = 'Sucesso', icon='padlock_closed.ico')    
    except: 
        sg.popup('Erro de conexão!', title = 'Erro', icon='padlock_closed.ico')
    
def send_message(message):
    try:
        message = IP + ': ' + message
        update_chat(message)
        client_socket.sendall(bytes(message, 'utf-8'))
    except: 
        sg.popup('Erro de conexão!', title = 'Erro', icon='padlock_closed.ico')
    
def update_chat(message):
    chat.append(message)   
    janela.find_element('chat').update(values = chat)

def get_current_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    IP = s.getsockname()[0]
    s.close()
    return IP
    
def create_layout():    
    layout = [
        [sg.Text('Meu IP:' + IP), sg.Text('IP:'), sg.Input(key='ip', do_not_clear=True, size=(25,25)), sg.Button('Conectar', key='conectar')],
        [sg.Listbox(key='chat', values = chat, size=(112, 25))],
        [sg.Input(key='mensagem', do_not_clear=False, size=(106,25)), sg.Button('Enviar', key='enviar')]
    ]
    return layout

chat = []
IP = get_current_ip()
server = threading.Thread(target=start_server)
server.start()

layout = create_layout()
janela = sg.Window('Encrypted chat', icon='padlock_closed.ico').Layout(layout)
while True:
    eventos, valores = janela.read()
    if eventos == sg.WINDOW_CLOSED:
        break
    if eventos == 'conectar':
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connect_client(valores['ip'])
    if eventos == 'enviar':
        send_message(valores['mensagem'])
