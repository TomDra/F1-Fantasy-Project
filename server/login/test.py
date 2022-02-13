import socket

"""
This is a test file for the login module.
Current requests:
[register, username, password]
[login, username, password]
[save_team, username, password, team_data, driver_data]
[return_team, username, password]
"""


def connect_to_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 9999))
    return s

"""connect to server and send login query to server"""
def login(username, password):
    s = connect_to_server()
    s.send(f'login-~-{username}-~-{password}'.encode())
    accept = s.recv(1024).decode()
    return [s,accept]

def register(username, password):
    s = connect_to_server()
    s.send(f'register-~-{username}-~-{password}'.encode())
    accept = s.recv(1024).decode()
    return accept

def send_teamData(username, password,team, drivers):
    s = connect_to_server()
    s.send(f'save_team-~-{username}-~-{password}-~-{team}-~-{drivers}'.encode())
    accept = s.recv(1024).decode()
    return accept

def recive_teamData(username, password):
    s = connect_to_server()
    s.send(f'return_team-~-{username}-~-{password}'.encode())
    data = s.recv(1024).decode()
    return data

print(register('test','test'))
print(send_teamData('test','test','test','test'))
print(recive_teamData('test','test'))
if (client := (login('test555', 'teststring99')))[1] == True:
    data = client[0].recv(1024).decode()
    print(data)
else:
    print(client)