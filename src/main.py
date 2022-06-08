from PySimpleGUI import PySimpleGUI as sg
from client_server import get_current_ip, thread_server, stop_server, connect_client, send_message
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
            update_key(values['encryption_method'], window)            
        if events == 'send':
            try:
                update_encryption(values['encryption_method'], values['key'])
                send_message(IP, values['client_ip'], values['message'], chat, window)
            except:
                sg.popup('Informe o IP da máquina que deseja conectar!', title = 'Erro', icon='padlock_closed.ico')
                
main()