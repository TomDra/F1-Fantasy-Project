import sqlite3
from argon2 import PasswordHasher
import socket
import threading
ph = PasswordHasher()
sqliteConnection = sqlite3.connect('logins.db', check_same_thread=False)
cursor = sqliteConnection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS logins (userID int NOT NULL,username string,hashpass string, UNIQUE(userID), PRIMARY KEY (userID));")
#cursor.execute(f'INSERT INTO logins VALUES (1,"test", "{ph.hash("teststring")}");')
print(cursor.execute("SELECT * FROM logins").fetchall())

class Account:
  def __init__(self,username):
    self.username = username
    try:
      if str(cursor.execute(f'SELECT username FROM logins WHERE username="{self.username}"').fetchall()[0]).split("'")[1] != None:
        self.account = True
        self.password_hash = str(cursor.execute(f'SELECT hashpass FROM logins WHERE username="{username}"').fetchall()[0]).split("'")[1]
    except IndexError:
      self.account = False

  def valid_account(self):
    return self.account

  def check_pass(self, given_pass):
    try:
      if ph.verify(self.password_hash, given_pass):
        return True
    except Exception:
      return [False,'Invalid Password']

  def create_record(self, password):
    id = 0
    while True:
      try:
        cursor.execute(f'Insert INTO logins VALUES({id},"{self.username}","{password}")')
        break
      except Exception:
        id = id + 1


def login(account_username, password):  
  user = Account(account_username)
  if user.valid_account():
    result = user.check_pass(password)
  else:
    result = [False,'Invalid Username']
  return result

def register(username, password):
  user = Account(username)
  if user.valid_account() != True:
    user.create_record(ph.hash(password))
    return True
  else:
    return [False,'Username Occupied']

"""create a new thread for each client and determine if the client is a new user or returning user so they can login or register"""
def handle_client_login(client_socket):
  request = client_socket.recv(1024).decode()
  request = request.split('-~-')
  print(request)
  if request[0] == 'register':
    result = register(request[1], request[2])
    client_socket.send(str(result).encode())
  elif request[0] == 'login':
    result = login(request[1], request[2])
    client_socket.send(str(result).encode())
    if result == True:
      return True
  else:
    client_socket.send(b'Invalid Request')
  client_socket.close()
  return False

def handle_client(client_socket):
  if handle_client_login(client_socket) == True:
    send_team_data(client_socket)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 9999))
s.listen(5)
"""create a thread for each client"""
while True:
  client_socket, address = s.accept()
  print(f'Connection from {address} has been established')
  client = threading.Thread(target=handle_client, args=(client_socket,))
  client.start()
  print(f'Thread for {address} has been created')
  client.join()
  sqliteConnection.commit()




sqliteConnection.close()