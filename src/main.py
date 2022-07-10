from PySimpleGUI import PySimpleGUI as sg
from DH import generate_public_key, generate_key
from client_server import get_current_ip, thread_server, stop_server, send_message
from layout import create_layout, update_key, update_encryption, update_public_key
           
def main():
    chat = []
    IP = get_current_ip()    

    layout = create_layout(IP, chat)
    window = sg.Window('Encrypted chat', layout, icon='padlock_closed.ico', finalize=True)
    thread_server(IP, chat, window) 
    
    while True:
        events, values = window.read()   
        if events == sg.WINDOW_CLOSED:
            if window['status_server'].DisplayText == 'online': stop_server(IP)
            break
        if events == 'start_server' and window['status_server'].DisplayText == 'offline':        
            thread_server(IP, chat, window) 
        if events == 'encryption_method':
            if values['key'] == '':
                key = update_key(values['encryption_method'], window)
            update_encryption(values['encryption_method'], key)
        if events == 'key':
            update_encryption(values['encryption_method'], values['key'])
        if events == 'P' or events == 'G' or events == 'A_private_key':
            public_key = generate_public_key(values['P'], values['G'], values['A_private_key'])
            update_public_key(public_key, window)
        if events == 'B_public_key':
            key = generate_key(values['P'], values['A_private_key'], values['B_public_key'])
            window['key'].update(key)
            update_encryption(values['encryption_method'], key)
        if events == 'send':
            send_message(values['client_ip'], values['message'], chat, window)
                
main()
