from PySimpleGUI import PySimpleGUI as sg
import socket
import threading

def start_server():
    IP = str(socket.gethostbyname_ex(socket.getfqdn())[2]).replace("'","").replace("[","").replace("]","")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((IP, 3000))
    s.listen()

    conn, addr = s.accept()
    while 1:
        data = conn.recv(1024)
        update_chat(data.decode('utf-8'))
        if not data:
            break
        conn.sendall(data)
    conn.close()

def connect_client(IP):
    client_socket.connect((IP, 3000))
    sg.popup('Conexão feita com sucesso!', title = 'Sucesso', icon='padlock_closed.ico')

def send_message(message):
    update_chat(message)
    client_socket.sendall(bytes(message, 'utf-8'))

def update_chat(message):
    chat.append(message)   
    janela.find_element('chat').update(values = chat)

chat = []
server = threading.Thread(target=start_server)
server.start()

layout = [
    [sg.Text('IP:'), sg.Input(key='ip', do_not_clear=True, size=(25,25)), sg.Button('Conectar', key='conectar')],
    [sg.Listbox(key='chat', values = chat, size=(112, 25))],
    [sg.Input(key='mensagem', do_not_clear=False, size=(106,25)), sg.Button('Enviar', key='enviar')]
]
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
