import socket

"""connect to server and send login query to server"""
def login(username, password):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 9999))
    s.send(f'login-~-{username}-~-{password}'.encode())
    accept = s.recv(1024).decode()
    return [s,accept]

def register(username, password):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 9999))
    s.send(f'register-~-{username}-~-{password}'.encode())
    accept = s.recv(1024).decode()
    return accept


if (client := (login('test', 'teststring99'))[1]) == True:
  data = client[0].recv(1024).decode()