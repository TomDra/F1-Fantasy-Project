import socket

"""connect to server and send login query to server"""
def login(username, password):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 9999))
    s.send(f'login-~-{username}-~-{password}'.encode())
    accept = s.recv(1024).decode()
    return accept

def register(username, password):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 9999))
    s.send(f'register-~-{username}-~-{password}'.encode())
    accept = s.recv(1024).decode()
    return accept

print(login('test', 'teststring99'))