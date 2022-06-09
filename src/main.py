from PySimpleGUI import PySimpleGUI as sg
from client_server import get_current_ip, thread_server, stop_server, send_message
from layout import create_layout, update_key, update_encryption
           
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
            key = update_key(values['encryption_method'], window)
            update_encryption(values['encryption_method'], key)
        if events == 'key':
            update_encryption(values['encryption_method'], values['key'])
        if events == 'send':
            send_message(IP, values['client_ip'], values['message'], chat, window)
                
main()
