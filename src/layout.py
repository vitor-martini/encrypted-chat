from PySimpleGUI import PySimpleGUI as sg
method = ''
key = ''

def update_chat(message, chat, window):
    chat.append(message)   
    window['chat'].update(values = chat)

def update_status(window, status):    
    window['status_server'].update(status)
    if status == 'online': window['status_server'].Update(text_color='forestgreen')
    if status == 'offline': window['status_server'].Update(text_color='firebrick')

def update_key(value, window):
    if value in ['S-DES', 'CBC']:
        key = '1000000000'
        window['key'].update(key)
        return key    
    if value == 'RC4':
        key = 'teste'
        window['key'].update(key)
        return key
        
def update_encryption(_method, _key):   
    global method, key 
    method = _method
    key = _key

def create_layout(IP, chat):    
    layout = [
        [sg.Text('Meu IP: ' + IP), sg.Text('Status servidor:'), sg.Text('offline', key = 'status_server', text_color='firebrick'), sg.Button('Hostear', key='start_server', size=(10,1))],
        [sg.Text('IP:'), sg.Input(key='client_ip', do_not_clear=True, size=(52,25))],
        [sg.Text('Criptografia:'), sg.Combo(key='encryption_method', values=['S-DES', 'CBC', 'RC4'], enable_events=True, size=(10,1)), sg.Text('Chave:'), sg.Input(key='key', do_not_clear=True, enable_events=True, size=(22,25))],
        [sg.Listbox(key='chat', values = chat, size=(55, 25))],
        [sg.Input(key='message', do_not_clear=False, size=(42,25)), sg.Button('Enviar', key='send', size=(10,1))]
    ]
    return layout