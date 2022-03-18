import socket,ast,datetime

def connect_to_chat_server():
    f = open('scripts/connect.private', 'r')    # Open the file containing the ip and port
    socket_connect = ast.literal_eval(f.read().replace('\n', ''))    # Read the file and convert it to a dictionary
    f.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket_connect[2], int(socket_connect[3])))
    return s


def output(chat_message, username):
    '''use sockets and to connect to the server and send the message'''
    s = connect_to_chat_server()
    time = datetime.datetime.now().strftime("%H:%M:%S")
    s.send(f'["send","[{time}] - {username}: {chat_message}"]'.encode())
    s.close()

def get_chats():
    '''use sockets and to connect to the server and get the messages'''
    s = connect_to_chat_server()
    s.send('["get_chats"]'.encode())
    chat_messages = s.recv(1024).decode()
    s.close()
    return chat_messages
